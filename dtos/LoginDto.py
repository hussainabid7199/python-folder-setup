from pydantic import BaseModel

class LoginDto(BaseModel):
    id: str
    name: str
    email: str
    token: str
