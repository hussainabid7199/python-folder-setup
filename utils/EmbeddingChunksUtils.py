from typing import List
from sentence_transformers import SentenceTransformer
from diInjector.diExtension import containers

class Embedding:
    def __init__(self):
        self.container = containers.Container()
        self.pine_cone = self.container.pine_cone()
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def generate_and_store_embedding(self, file_id: str, text: str, metadata: dict = None):
        try:
            # Generate the text embedding
            embedding = self.model.encode(text, show_progress_bar=False).tolist()
            print(f"Embedding generated for doc_id: {file_id}, length: {len(embedding)}")

from bucket.PineConeBucket import getPinecone

model = SentenceTransformer("all-MiniLM-L6-v2")
index = getPinecone()
if index is None:
    raise ValueError("Failed to initialize Pinecone index. Check API key and environment settings.")


def generate_and_store_embedding(file_id: str, text: str, metadata: dict = None):
    try:

        embedding = model.encode(text, show_progress_bar=False).tolist()
        print(
            f"Embedding generated for doc_id: {file_id}, length: {len(embedding)}")

            # Upsert the embedding into Pinecone
            upsert_response = self.pine_cone.getPinecone().upsert(
                vectors=[{"id": file_id, "values": embedding}]
            )
            print(f"Upsert response: {upsert_response}")

            return {"status": "success", "doc_id": file_id}

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def generate_and_store_chunks_embedding(self, file_id: str, chunks: List[str]):
            for i, chunk in enumerate(chunks):
                chunk_id = f"{file_id}_chunk_{i}"
                result = self.generate_and_store_embedding(chunk_id, chunk)

                if result["status"] == "error":
                    return result

            return {"status": "success", "doc_id": file_id, "num_chunks": len(chunks)}

   
