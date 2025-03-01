# from pydantic import BaseModel

# class UploadModel(BaseModel):
#     filename: str
#     content: str

from fastapi import UploadFile
from pydantic import BaseModel

class UploadModel(BaseModel):
    filename: str
    content: str
    file: UploadFile
