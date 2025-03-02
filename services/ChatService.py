import os
import sys
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from bucket.OpenSearchBucket import OpenSearchBucket
from bucket.PineConeBucket import getPinecone
from dtos.ChatDto import ChatDto
from interface.IChatInterface import IChatService
from models.ChatModel import ChatModel
from utils.ChunkTextUtils import chunk_text
from utils.EmbeddingChunksUtils import generate_and_store_chunks_embedding
from bucket.AWSBucket import AWSbucket
from sentence_transformers import SentenceTransformer
from utils.GenerateAnswerUtils import generate_answer_from_query
import logging

# Configure Logger (only logs to terminal)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

dotenv_path = ".env"
load_dotenv(dotenv_path=dotenv_path)

bucket_name = os.getenv("BUCKET_NAME")

class ChatService(IChatService):
    def __init__(self):
        aws_bucket = AWSbucket()
        self.s3_client = aws_bucket.get_aws_bucket()
        self.bucket_name = bucket_name

        # Initialize Pinecone
        self.pinecone_index = getPinecone()

        # Initialize OpenSearch
        self.opensearch_client = OpenSearchBucket().get_client()

        # Debug: Verify clients
        logger.info(f"Pinecone index type: {type(self.pinecone_index)}")
        logger.info(f"OpenSearch client type: {type(self.opensearch_client)}")
    
    def chat(self, model: ChatModel) -> ChatDto:
        try:
            query = model.query
            model = SentenceTransformer("all-MiniLM-L6-v2")
            # Step 1: Generate embedding for user query
            embedded_query = model.encode(query, show_progress_bar=False).tolist()
            
            # Step 2: Perform semantic search in Pinecone
            pinecone_result = self.pinecone_index.query(vector=embedded_query, top_k=5,include_metadata=True)
            chunks = [match["metadata"]['chunk'] for match in pinecone_result['matches']]
            
            # Step 3: Perform keyword search in OpenSearch
            user_query = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["chunk"] 
                    }
                },
                "size": 5  # Match Pinecone's top_k
            }
            opensearch_result = self.opensearch_client.search(index="pdf_chunks",body=user_query)
            result = [hit["_source"]["chunk"] for hit in opensearch_result["hits"]["hits"]]
            
            # Step 4: Combine results (remove duplicates and rank them)
            combined_chunks = list(set(chunks + result))
            
            # Step 5: Pass combined results to LLM
            llm_response = generate_answer_from_query(query, combined_chunks)
            
            return ChatDto(response=llm_response)
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))