from operator import index
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

from bucket.PineConeBucket import getPinecone

model = SentenceTransformer("all-MiniLM-L6-v2")
index = getPinecone()
if index is None:
    raise ValueError("Failed to initialize Pinecone index. Check API key and environment settings.")


def generate_and_store_embedding(file_id: str, chunk: str):
    try:

        embedding = model.encode(chunk, show_progress_bar=False).tolist()
        print(f"Embedding generated for doc_id: {file_id}, length: {len(embedding)}")

        # upsert_response = index.upsert(
        #     vectors=[{"id": file_id, "values": embedding},"metadata": {"chunk": chunk}]
        # )
        vectors = [
            {
                "id": f"file_id_{file_id}",  
                "values": embedding,  
                "metadata": {"chunk": chunk}  
            }
        ]

        upsert_response = index.upsert(vectors=vectors)  # Or use `items=vectors` if needed

        print(f"Upsert response: {upsert_response}")

        return {"status": "success", "doc_id": file_id}

    except Exception as e:
        return {"status": "error", "error": str(e)}


def generate_and_store_chunks_embedding(file_id: str, chunks: List[str]):
    try:
        for i, chunk in enumerate(chunks):
            chunk_id = f"{file_id}_chunk_{i}"
            result = generate_and_store_embedding(chunk_id, chunk)

            if result["status"] == "error":
                return result

        return {"status": "success", "doc_id": file_id, "num_chunks": len(chunks)}

    except Exception as e:
        return {"status": "error", "error": str(e)}
