from fastapi import APIRouter, Depends, File, UploadFile
from dependency_injector.wiring import inject, Provide
from diInjector.diExtension import Container
from dtos.ResponseDto import ResponseDto
from dtos.UploadDto import UploadDto
from interface.IUploadInterface import IUploadService
from models.UploadModel import UploadModel
import logging

uploadRouter = APIRouter()

@uploadRouter.post("/upload", response_model=ResponseDto[dict])
@inject
async def upload(
    file: UploadFile = File(...),
    upload_service: IUploadService = Depends(Provide[Container.upload_service]),
):
    # Read file content for processing
    content = await file.read()
    await file.seek(0)  # reset pointer in case needed later
    # Create an UploadModel instance manually (note: we're decoding binary content to a string)
    model = UploadModel(
        filename=file.filename, 
        content=content.decode("latin-1"), 
        file=file
    )
    # Call the asynchronous upload service
    service_response = await upload_service.upload(file, model)
    
    return ResponseDto(
        message="File Uploaded Successfully", 
        status=200
    )
