from mongoengine import Document, StringField, BooleanField, connect
import os
from dotenv import load_dotenv

dotenv_path = ".env"
load_dotenv(dotenv_path=dotenv_path)

MONGO_DB_URI = os.getenv("MONGO_DB_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

connect(MONGO_DB_NAME, host=MONGO_DB_URI)
print(connect)

class User(Document):
    name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    is_verified = BooleanField(required=True)
    otp = StringField(required=True)
