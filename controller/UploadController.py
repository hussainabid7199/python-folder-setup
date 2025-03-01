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
    
    service_response = await upload_service.upload(file);
    return ResponseDto(
        message="File Uploaded Successfully", status=200, data=service_response
    )
