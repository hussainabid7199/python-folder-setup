import os
import numpy as np
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

dotenv_path = "backend\.env"
load_dotenv(dotenv_path=dotenv_path)

api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_ENVIRONMENT")

if not api_key or not isinstance(api_key, str):
    raise ValueError("PINECONE_API_KEY must be set and should be a valid string.")

pinecone = Pinecone(api_key=api_key)

INDEX_NAME = "pdf-search-index"
if not isinstance(INDEX_NAME, str):
    raise ValueError("INDEX_NAME must be a valid string.")

def getPinecone():
    try:
        existing_indexes = [index.name for index in pinecone.list_indexes()]
        if INDEX_NAME not in existing_indexes:
            print(f"Creating index: {INDEX_NAME}")
            pinecone.create_index(
                name=INDEX_NAME,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region=environment,
                ),
            )
            print(f"Using index: {INDEX_NAME}")
            return pinecone.Index(INDEX_NAME)
    except Exception as e:
        print(f"Error during index setup: {e}")
        raise
