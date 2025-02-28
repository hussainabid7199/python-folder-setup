from fastapi import UploadFile
from pydantic import BaseModel, field_validator
from utils.CheckFileTypeUtils import check_pdf_type

class UploadDto(BaseModel):
    file: UploadFile
    
    @field_validator("file")
    @classmethod
    def validate_file(cls, file: UploadFile):
        return check_pdf_type(file)