from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel

class UploadModel(BaseModel):
    filename: Optional[str] = None
    content: Optional[str] = None
    file: Optional[UploadFile] = None
