from pydantic import BaseModel

class RegisterDto(BaseModel):
    username: str
    email: str
    password: str