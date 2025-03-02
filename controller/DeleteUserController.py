from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from diInjector.diExtension import Container
from dtos.ResponseDto import ResponseDto
from interface.IDeleteUserInterface import IDeleteUserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
DeleteUserRouter = APIRouter()

@DeleteUserRouter.delete("/delete_user", response_model=ResponseDto)
@inject
def deleteuser(
    token: str = Depends(oauth2_scheme),
    deleteuser_service: IDeleteUserService = Depends(Provide[Container.deleteuser_service])
):
    service_response = deleteuser_service.deleteuser(token)
    return ResponseDto(
        message="User Deleted Successfully", status=200, data=service_response
    )
