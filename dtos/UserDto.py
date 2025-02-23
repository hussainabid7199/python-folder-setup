from pydantic import BaseModel

class UserDto(BaseModel):
    id: str
    name: str
    email: str