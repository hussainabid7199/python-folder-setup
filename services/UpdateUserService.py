import os
import bcrypt
from bson import ObjectId
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
import jwt
from pymongo import ReturnDocument
from dtos.UpdateUserDto import UpdateUserDto
from interface.IUpdateUserInterface import IUpdateUserService
from models.UpdateUserModel import UpdateUserModel

dotenv_path=".env"
load_dotenv(dotenv_path=dotenv_path)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UpdateUserService(IUpdateUserService):
    def __init__(self, db):
        self.db = db
        self.db = db.get_collection("users")

    def updateuser(self, model: UpdateUserModel, token: str = Depends(oauth2_scheme)) -> UpdateUserDto:

            token = token.strip()
            token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = token.get('sub')

            if not user_id:
                raise HTTPException(status_code=404, detail="User Id Not Found")

            obj_id = ObjectId(user_id)
            if not obj_id:
                raise HTTPException(status_code=400, detail="User Id is in invalid format")

            hashedpassword = bcrypt.hashpw(model.password.encode("utf-8"), bcrypt.gensalt())
            
            updated_data = {}
            if model.name:
                updated_data["name"] = model.name
            
            if model.email:
                updated_data["email"] = model.email
            
            if model.password:
                updated_data["password"] = hashedpassword

            if not updated_data:
                raise HTTPException(status_code=200, detail="Nothing to update")
            
            user = self.db.find_one_and_update(
                {"_id": obj_id}, {
                    "$set": updated_data
                },
                return_document=ReturnDocument.AFTER
            )

            if not user:
                raise HTTPException(status_code=400, detail="Updaation failed")
    
            user["_id"] = str(user["_id"])
            data = jsonable_encoder(user)

            update_dto = UpdateUserDto(
                id= data["_id"],
                name = data["name"],
                email = data["email"]
            )

            return update_dto
