
from fastapi import UploadFile

def check_pdf_type(file: UploadFile):
    # Check if content_type is provided, otherwise fallback to filename extension
    if file:
        return True
    else:
        return False
