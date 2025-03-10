from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from gridfs import GridFS

# load_dotenv()
dotenv_path = ".env"
load_dotenv(dotenv_path=dotenv_path)

# initalize mongodb
MONGO_DB_URI = os.getenv('MONGO_DB_URI')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')

class dbConnection:
    def __init__(self):
        """Initialize MongoDB connection"""
        self.client = MongoClient(MONGO_DB_URI)
        self.db = self.client.MONGO_DB_NAME  # Replace with your database name
        self.gridfs = GridFS(self.db)  # Initialize GridFS

    def get_db(self):
        print(self.db)
        return self.db

    def get_gridfs(self):
        """Return GridFS instance"""
        return self.gridfs

    def create_collection(self, collection_name):
        if collection_name not in self.db.list_collection_names():
            self.db.create_collection(collection_name)
            print(f"Creating collection '{collection_name}'")
        else:
            print("Collection '{collection_name}' already exists")
            return self.db[collection_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]
