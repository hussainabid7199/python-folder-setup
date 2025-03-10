import random
import string
from typing import Dict
import bcrypt
from fastapi import BackgroundTasks, HTTPException
from db.collection.UserCollection import UserCollection
from dtos.ResponseDto import ResponseDto
from dtos.UserDto import UserDto
from interface.IAccountInterface import IAccountService
from jwtConfig.jwtConfig import JWTConfig
from models.LoginModel import LoginModel
from models.RegisterModel import RegisterModel
from utils.SendEmailsUtils import send_email
from utils.GetTemplateUtils import get_email_template
from schema.RegisterSchema import validator

class AccountService(IAccountService):
    def __init__(self, db):
        self.db = db.get_collection('users')

    def register(self, model: RegisterModel) -> UserDto:
        model_dict = model.model_dump()

        if not validator.validate(model_dict):
            raise HTTPException(status_code=500, detail=validator.errors)

        existing_user = self.db.find_one({"email": model.email})
        if  existing_user:
            raise HTTPException(status_code=400, detail="User found with this email")

        hashedPassword = bcrypt.hashpw(model.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        code = "".join(random.choices(string.digits, k=6))
        print(f'code: {code}')

        user_data = {
            "name": model.name,
            "email": model.email,
            "password": hashedPassword,
            "is_verified": False
        }

        response = self.db.insert_one(user_data)

        user_dto = UserDto(
            id = str(response.inserted_id),
            name = model.name,
            email= model.email,
        )

        email_body = get_email_template("otp_template.html", name=model.name, code=code)
        print(email_body)

        send_email(model.email, email_body)
        print(f"email: {model.email}",{email_body})
        return user_dto;

    def login(self, model: LoginModel) -> UserDto:
        existing_user = self.db.find_one({"email": model.email})

        if existing_user is None:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        existing_user["id"] = str(existing_user["_id"])
        del existing_user["_id"]

        password_hash = existing_user.get("password")
        if not password_hash or not bcrypt.checkpw(model.password.encode("utf-8"), password_hash.encode("utf-8")):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        token = JWTConfig.generate_token(existing_user["email"], existing_user["id"])

        user_dto = UserDto(id=existing_user["id"],name=existing_user.get("name", ""),email=existing_user["email"],token=token)

        return user_dto
