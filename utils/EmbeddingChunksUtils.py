from operator import index
from typing import List
from sentence_transformers import SentenceTransformer

from bucket.PineConeBucket import getPinecone
from db.connection import dbConnection

model = SentenceTransformer("all-MiniLM-L6-v2")
index = getPinecone()
if index is None:
    raise ValueError("Failed to initialize Pinecone index. Check API key and environment settings.")

db = dbConnection()

def generate_and_store_embedding(file_id: str, text: str, metadata: dict = None):
    try:

        embedding = model.encode(text, show_progress_bar=False).tolist()
        print(
            f"Embedding generated for doc_id: {file_id}, length: {len(embedding)}")
        
        metadata = metadata or {}
        metadata.update({"file_id": file_id, "chunks": text[:500]})

        chunk_collections = db.get_collection("metadata")
        metadata_store = chunk_collections.insert_one(metadata)

        upsert_response = index.upsert(
            vectors=[{"id": file_id, "values": embedding}]
        )
        print(f"Upsert response: {upsert_response}")

        return {"status": "success", "doc_id": file_id, "chunk_collection": metadata_store}

    except Exception as e:
        return {"status": "error", "error": str(e)}


def generate_and_store_chunks_embedding(file_id: str, chunks: List[str]):
    try:
        for i, chunk in enumerate(chunks):
            chunk_id = f"{file_id}"
            result = generate_and_store_embedding(chunk_id, chunk)

            if result["status"] == "error":
                return result

        return {"status": "success", "doc_id": file_id, "num_chunks": len(chunks)}

    except Exception as e:
        return {"status": "error", "error": str(e)}
