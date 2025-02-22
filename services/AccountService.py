from typing import Dict
import bcrypt
from fastapi import HTTPException
from dtos.RegisterDto import RegisterDto
from interface.IAccountInterface import IAccountService

class AccountService(IAccountService):
    def __init__(self, db):
        self.db = db.get_collection('users')

    def register(self, user_data: RegisterDto) -> Dict:
        exsisting_user = self.db.find_one({"email": user_data.email})
        if  exsisting_user:
            raise HTTPException(status_code=400, detail="User found with this email")
        
        
        hashedPassword = bcrypt.hashpw(user_data.password.encode("utf-8"), bcrypt.gensalt())
        user_data = {
            "useranme": user_data.username,
            "email": user_data.email,
            "password": hashedPassword.decode("utf-8"),
            "is_verified": False
        }
        
        new_user = self.db.insert_one(user_data)
        return {
            "status": 200,
            "message": "User Registered successfully",
            "new_user": str(new_user.inserted_id),
        }
   
    def login(self, credentials: Dict) -> Dict:
        # Validate user credentials (Example)
        for user in self.db:
            if user["email"] == credentials["email"]:
                return {"message": "Login successful", "user": user}
        return {"error": "Invalid credentials"}
