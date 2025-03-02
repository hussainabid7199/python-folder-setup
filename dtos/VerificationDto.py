from pydantic import BaseModel

class VerificationDto(BaseModel):
     email: str
     token: str