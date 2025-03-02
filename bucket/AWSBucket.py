from dotenv import load_dotenv
import boto3
import os


dotenv_path = ".env"
load_dotenv(dotenv_path)

# aws_access_Key = os.getenv("ACCESS_AWS_SECURITY_KEY_ID")
# aws_secret_access_Key = os.getenv("ACCESS_AWS_KEY_ID")
# bucketName = os.getenv("BUCKET_NAME")
# region = "us-east-1"


# class AWSbucket:
#     def get_aws_bucket(self):
#         """Initialize S3 client and validate bucket existence"""

#         if not aws_access_Key or not aws_secret_access_Key:
#             raise ValueError("AWS credentials are missing")
        
#         s3 = boto3.client(
#             "s3",
#             aws_access_key_id=aws_access_Key,
#             aws_secret_access_key=aws_secret_access_Key,
#             region_name=region,
#         )

#         bucket_name = bucketName

#         buckets = [bucket["Name"] for bucket in s3.list_buckets()["Buckets"]]

#         if bucket_name in buckets:
#             print(f"Bucket '{bucket_name}' exists!")
#         else:
#             print(f"Bucket '{bucket_name}' not found.")
            
#         s3_resource = boto3.resource(
#             "s3",
#             aws_access_key_id=aws_access_Key,
#             aws_secret_access_key=aws_secret_access_Key,
#             region_name=region,
#         )

#         bucket = s3_resource.Bucket(bucket_name)
#         print(f"Bucket retrieved: {bucket.name}")

class AWSbucket:
    def get_aws_bucket(self):
        """Initialize S3 client and validate bucket existence"""
        aws_access_Key = os.getenv("ACCESS_AWS_SECURITY_KEY_ID")
        aws_secret_access_Key = os.getenv("ACCESS_AWS_KEY_ID")
        bucketName = os.getenv("BUCKET_NAME")
        region = "us-east-1"

        # Ensure credentials are loaded
        if not aws_access_Key or not aws_secret_access_Key:
            raise ValueError("AWS credentials are missing. Check your .env file.")

class awsBucket:
    def get_aws_bucket(self):
        try:
            s3 = boto3.client(
                "s3",
                aws_access_key_id=aws_access_Key,
                aws_secret_access_key=aws_secret_access_Key,
                region_name=region,
            )

            # Check if bucket exists
            existing_buckets = [bucket["Name"] for bucket in s3.list_buckets()["Buckets"]]
            if bucketName not in existing_buckets:
                raise ValueError(f"Bucket '{bucketName}' does not exist.")

            print(f"Bucket '{bucketName}' found!")

            return s3  # Return the initialized client for future use

        except Exception as e:
            raise RuntimeError(f"Error initializing AWS S3: {str(e)}")