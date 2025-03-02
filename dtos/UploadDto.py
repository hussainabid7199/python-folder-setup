
from pydantic import BaseModel
from typing import List

class UploadDto(BaseModel):
    message: str
    status: int