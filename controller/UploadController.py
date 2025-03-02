from fastapi import APIRouter, Depends, File, UploadFile
from dependency_injector.wiring import inject, Provide
from diInjector.diExtension import Container
from dtos.ResponseDto import ResponseDto
from dtos.UploadDto import UploadDto
from exceptions.CustomError import custom_error
from interface.IUploadInterface import IUploadService
from models.UploadModel import UploadModel
import logging

uploadRouter = APIRouter()

@uploadRouter.post("/upload", response_model=ResponseDto[UploadDto], status_code=201)
@inject
async def upload(
    file: UploadFile = File(...),
    upload_service: IUploadService = Depends(Provide[Container.upload_service]),
):
    try:
        service_response = await upload_service.upload(file)
        return ResponseDto(
            message="File Uploaded Successfully", 
            status="success",
            statusCode=201,
            data=service_response
        )
    except Exception as e:
        return custom_error(e)
