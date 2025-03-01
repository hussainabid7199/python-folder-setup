from fastapi import UploadFile
from pydantic import BaseModel, field_validator
from utils.CheckFileTypeUtils import check_pdf_type

class UploadDto(BaseModel):
    file: UploadFile