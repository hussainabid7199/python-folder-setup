from pydantic import BaseModel


class FindUserDto(BaseModel):
    id: str
    name: str
    email: str
    is_verified: bool
