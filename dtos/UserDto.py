from typing import Optional
from pydantic import BaseModel

class UserDto(BaseModel):
    id: str;
    name: str;
    email: str;
    token: Optional[str] = "";