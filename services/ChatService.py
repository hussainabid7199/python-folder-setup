import os
from dotenv import load_dotenv
from interface.IChatInterface import IChatService

dotenv_path = ".env"
load_dotenv(dotenv_path=dotenv_path)

bucket_name = os.getenv("BUCKET_NAME")

class ChatService(IChatService):
      def __init__(self, db, aws_bucket, pine_cone):
        self.db = db
        self.aws_bucket = aws_bucket
        self.pine_cone = pine_cone
        self.s3_client = aws_bucket
        self.bucket_name = bucket_name