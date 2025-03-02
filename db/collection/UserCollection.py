from mongoengine import Document, StringField, BooleanField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField
from mongoengine import connect
import os
from dotenv import load_dotenv

dotenv_path = ".env"
load_dotenv(dotenv_path=dotenv_path)

MONGO_DB_URI = os.getenv("MONGO_DB_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

connect(MONGO_DB_NAME, host=MONGO_DB_URI)

class VerificationCode(EmbeddedDocument):
    code = StringField(required=True)
    expiryTime = DateTimeField(required=True)

class UserCollection(Document):
    name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    is_verified = BooleanField(required=True)
    verification_code = EmbeddedDocumentField(VerificationCode)
