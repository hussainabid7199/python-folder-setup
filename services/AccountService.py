from typing import Dict
import bcrypt
from fastapi import HTTPException
from db.collection.UserCollection import UserCollection
from dtos.ResponseDto import ResponseDto
from dtos.UserDto import UserDto
from interface.IAccountInterface import IAccountService
from models.RegisterModel import RegisterModel

class AccountService(IAccountService):
    def __init__(self, db):
        self.db = db.get_collection('users')

    def register(self, model: RegisterModel) -> UserDto:
        exsisting_user = self.db.find_one({"email": model.email})
        if  exsisting_user:
            raise HTTPException(status_code=400, detail="User found with this email")
        
        
        hashedPassword = bcrypt.hashpw(model.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8");
        
        user_data = {
            "name": model.name,
            "email": model.email,
            "password": hashedPassword,
            "is_verified": False
        }

        # result = UserCollection();
        # result.name = model.username
        
        response: UserDto = self.db.insert_one(user_data);
        return response;
   
    def login(self, credentials: Dict) -> Dict:
        # Validate user credentials (Example)
        for user in self.db:
            if user["email"] == credentials["email"]:
                return {"message": "Login successful", "user": user}
        return {"error": "Invalid credentials"}
