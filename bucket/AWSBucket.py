from dotenv import load_dotenv
import boto3
import os


dotenv_path = ".env"
load_dotenv(dotenv_path)

aws_access_Key = os.getenv("ACCESS_AWS_SECURITY_KEY_ID")
aws_secret_access_Key = os.getenv("ACCESS_AWS_KEY_ID")
bucketName = os.getenv("BUCKET_NAME")
region = "us-east-1"


class AWSbucket:
    def get_aws_bucket(self):
        s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_Key,
            aws_secret_access_key=aws_secret_access_Key,
            region_name=region,
        )

        bucket_name = bucketName

        buckets = [bucket["Name"] for bucket in s3.list_buckets()["Buckets"]]

        if bucket_name in buckets:
            print(f"Bucket '{bucket_name}' exists!")
        else:
            print(f"Bucket '{bucket_name}' not found.")
            
        s3_resource = boto3.resource(
            "s3",
            aws_access_key_id=aws_access_Key,
            aws_secret_access_key=aws_secret_access_Key,
            region_name=region,
        )

        bucket = s3_resource.Bucket(bucket_name)
        print(f"Bucket retrieved: {bucket.name}")
