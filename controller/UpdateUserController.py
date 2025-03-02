from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from diInjector.diExtension import Container
from dtos.ResponseDto import ResponseDto
from dtos.UpdateUserDto import UpdateUserDto
from interface.IUpdateUserInterface import IUpdateUserService
from models.UpdateUserModel import UpdateUserModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

UpdateUserRouter = APIRouter()

@UpdateUserRouter.patch("/update_user", response_model=ResponseDto[UpdateUserDto])
@inject
def updateuser(
    model: UpdateUserModel, 
    token: str = Depends(oauth2_scheme),
    updateuser_service: IUpdateUserService = Depends(Provide[Container.updateuser_service])
):
    service_response = updateuser_service.updateuser(model, token)
    return ResponseDto(
        message="User Detail update successsfully", status=200, data=service_response
    )
