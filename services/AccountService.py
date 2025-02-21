from typing import Dict
from interface.IAccountInterface import IAccountService

class AccountService(IAccountService):
    def __init__(self, db):
        self.db = db

    def register(self, user_data: Dict) -> Dict:
        # Save user to database (Example)
        user = {"id": 1, "email": user_data["email"], "name": user_data["name"]}
        self.db.append(user)  # Simulating DB insertion
        return {"message": "User registered successfully", "user": user}

    def login(self, credentials: Dict) -> Dict:
        # Validate user credentials (Example)
        for user in self.db:
            if user["email"] == credentials["email"]:
                return {"message": "Login successful", "user": user}
        return {"error": "Invalid credentials"}
