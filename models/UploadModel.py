from fastapi import File, UploadFile
from pydantic import BaseModel, FilePath

class UploadModel(BaseModel):
    file: UploadFile = File(...)