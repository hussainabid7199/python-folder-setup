import os
import sys
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from dtos.ChatDto import ChatDto
from interface.IChatInterface import IChatService
from models.ChatModel import ChatModel
from utils.CheckFileTypeUtils import check_pdf_type
from utils.ChunkTextUtils import chunk_text
from utils.EmbeddingChunksUtils import generate_and_store_chunks_embedding
from utils.PdfProccessingUtils import extract_text_from_pdf
from bucket.AWSBucket import AWSbucket

dotenv_path = ".env"
load_dotenv(dotenv_path=dotenv_path)

bucket_name = os.getenv("BUCKET_NAME")

class ChatService(IChatService):
    def __init__(self):
        aws_bucket = AWSbucket()

        self.s3_client = aws_bucket.get_aws_bucket()
        self.s3_client = bucket_name