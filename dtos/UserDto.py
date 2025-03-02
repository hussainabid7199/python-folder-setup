from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CodeDto(BaseModel):
    code: str;
    expiryTime: datetime;

class UserDto(BaseModel):
    id: str;
    name: str;
    email: str;
    verification_code: CodeDto
    token: Optional[str] = "";