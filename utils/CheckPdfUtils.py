from fastapi import UploadFile

def check_pdf_type(file: UploadFile):
    if file.content_type != "application/pdf":
        raise ValueError("Please upload only pdf files we accept only pdf")
    return file