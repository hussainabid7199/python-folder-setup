from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from diInjector.diExtension import Container
from dtos.ResponseDto import ResponseDto
from dtos.UploadDto import UploadDto
from interface.IUploadInterface import IUploadService
from models.UploadModel import UploadModel

UploadRouter = APIRouter()

@UploadRouter.post("/upload", response_model=ResponseDto[UploadDto])
@inject
def upload(
    model: UploadModel,
    upload_service: IUploadService = Depends(Provide[Container.upload_service]),
):
    service_response = upload_service.upload(model)
    return ResponseDto(
        message="File Uploaded Successfully", status=200, data=service_response
    )
