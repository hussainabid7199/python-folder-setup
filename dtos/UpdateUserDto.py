from typing import Optional
from pydantic import BaseModel

class UpdateUserDto(BaseModel):
    id: str
    name: Optional[str]
    email: Optional[str]