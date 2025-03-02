from operator import index
from typing import List
from sentence_transformers import SentenceTransformer
from bucket.PineConeBucket import pineCone

model = SentenceTransformer("all-MiniLM-L6-v2")
index = pineCone.getPinecone()
if index is None:
    raise ValueError("Failed to initialize Pinecone index. Check API key and environment settings.")

class embed:

    def generate_and_store_embedding(self, file_id: str, text: str):
        def __init__(self):
            self.file_id = file_id
            self.text = text
        
        try:
            print(f"PineCone instance: {self.pine_cone}")
            embedding = model.encode(text, show_progress_bar=False).tolist()
            print(f"Embedding generated for doc_id: {file_id}, length: {len(embedding)}")

            upsert_response = index.upsert(vectors=[{"id": file_id, "values": embedding}])
        
            print(f"Upsert response: {upsert_response}")

            return {"status": "success", "doc_id": file_id}

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def generate_and_store_chunks_embedding(self, file_id: str, chunks: List[str]):
        try:
            for i, chunk in enumerate(chunks):
                chunk_id = f"{file_id}_{i}"
                result = embed.generate_and_store_embedding(self, chunk_id, chunk)

                if result["status"] == "error":
                    return result

            return {"status": "success", "doc_id": file_id, "num_chunks": len(chunks)}

        except Exception as e:
            return {"status": "error", "error": str(e)}

