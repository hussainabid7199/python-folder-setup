import os
from bucket.OpenSearchBucket import OpenSearchBucket

# Initialize OpenSearch connection
opensearch_client = OpenSearchBucket().get_client()
index_name = os.getenv("OPENSEARCH_INDEX", "pdf_chunks")

def index_document(document):
    """Indexes a document into OpenSearch."""
    try:
        response = opensearch_client.index(
            index=index_name,
            body=document
        )
        return {"status": "success", "result": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def search_keyword(index_name, query):
    """Performs keyword-based search."""
    query = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["chunk"]  # Adjust field name if different
                    }
                },
                "size": 5  # Match Pinecone's top_k
            }
    try:
        response = opensearch_client.search(index=index_name, body=query)
        return [hit["_source"]["content"] for hit in response["hits"]["hits"]]
    except Exception as e:
        return {"status": "error", "message": str(e)}
