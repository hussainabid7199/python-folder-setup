from pydantic import BaseModel

class VerificationModel(BaseModel):
    email: str
    code: str