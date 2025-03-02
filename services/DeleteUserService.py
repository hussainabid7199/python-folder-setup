from bson import ObjectId
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from interface.IDeleteUserInterface import IDeleteUserService
import os

dotenv_path=".env"
load_dotenv(dotenv_path=dotenv_path)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class DeleteUserService(IDeleteUserService):
    def __init__(self, db):
        self.db =db
        self.db = db.get_collection("users")

    def deleteuser(self, token: str = Depends(oauth2_scheme)):
        token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = token.get("sub")

        if not user_id:
            raise HTTPException(status_code=404, detail="User id not found")

        obj_id = ObjectId(user_id)
        if not obj_id:
            raise HTTPException(status_code=500, detail="Cannot convert into object")

        self.db.delete_one({"_id": obj_id})

        
