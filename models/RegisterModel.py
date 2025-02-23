from pydantic import BaseModel

class RegisterModel(BaseModel):
    name: str
    email: str
    password: str