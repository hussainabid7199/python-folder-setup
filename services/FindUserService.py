import os
from bson import ObjectId
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
import jwt
from dtos.FindUserDto import FindUserDto
from interface.IFindUserInterface import IFindUserService
from dotenv import load_dotenv

# env
dotenv_path=".env"
load_dotenv(dotenv_path=dotenv_path)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class FindUserService(IFindUserService):
    def __init__(self, db):
        self.db = db
        self.db = db.get_collection('users')

    def finduser(self, token: str = Depends(oauth2_scheme)) -> FindUserDto:
        try:
            token = token.strip()
            token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = token.get('sub')

            if not user_id:
                raise HTTPException(status_code=404, detail="User Id Not Found")

            obj_id = ObjectId(user_id)
            if not obj_id:
                raise HTTPException(status_code=400, detail="User Id is in invalid format")

            user = self.db.find_one({"_id": obj_id})
            if not user:
                raise HTTPException(status_code=404, detail="User not found with this Id")

            user["_id"] = str(user["_id"])
            user_data = jsonable_encoder(user)

            user_dto = FindUserDto(
                id = user_data["_id"],
                name = user_data["name"],
                email = user_data["email"],
                is_verified = user_data["is_verified"]
            )

            return user_dto

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=404, detail="Token Expired")
