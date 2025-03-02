import os
import boto3
from dotenv import load_dotenv
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

dotenv_path = ".env"
load_dotenv(dotenv_path)

class OpenSearchBucket:
    def __init__(self):
        self.host = os.getenv("OPEN_SEARCH_HOST")  # OPEN_SEARCH_HOST
        self.region = os.getenv("AWS_REGION")  # AWS_REGION
        self.service = "es"  # OpenSearch uses 'es' for service name

        aws_access_key = os.getenv("ACCESS_AWS_SECURITY_KEY_ID")
        aws_secret_key = os.getenv("ACCESS_AWS_KEY_ID")

        if not aws_access_key or not aws_secret_key:
            raise ValueError("AWS credentials not found. Check your .env file.")

        # Initialize AWS authentication
        self.auth = AWS4Auth(
            aws_access_key, aws_secret_key, self.region, self.service
        )

        # Initialize OpenSearch client
        self.client = OpenSearch(
            hosts=[{"host": self.host, "port": 443}],
            http_auth=self.auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )

    def get_client(self):
        return self.client
