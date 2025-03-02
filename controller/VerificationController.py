from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from diInjector.diExtension import Container
from dtos.ResponseDto import ResponseDto
from dtos.VerificationDto import VerificationDto
from interface.IVerificationInterface import IVerificationService
from models.VerificationModel import VerificationModel

VerificationRouter = APIRouter()

@VerificationRouter.post("/verify_email", response_model=ResponseDto[VerificationDto])
@inject
def verify(
    model: VerificationModel,
    verification_service: IVerificationService = Depends(Provide[Container.verification_service]),
):
    service_response = verification_service.verify(model)
    return ResponseDto(
        message = "User Verified Successfully.Now you can log in", status= 200, data=service_response,
    )