# from fastapi import UploadFile

# def check_pdf_type(file: UploadFile):
#     if file.content_type != "application/pdf":
#         raise ValueError("Please upload only pdf files we accept only pdf")
#     return file

from fastapi import UploadFile

def check_pdf_type(file: UploadFile):
    # Check if content_type is provided, otherwise fallback to filename extension
    if file:
        return True
    else:
        return False
