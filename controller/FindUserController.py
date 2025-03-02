

from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from diInjector.diExtension import Container
from dtos.FindUserDto import FindUserDto
from dtos.ResponseDto import ResponseDto
from interface.IFindUserInterface import IFindUserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

FindUserRouter = APIRouter()

@FindUserRouter.get("/find_user", response_model=ResponseDto[FindUserDto])
@inject
def finduser(
    token: str = Depends(oauth2_scheme),
    finduser_service: IFindUserService = Depends(Provide[Container.finduser_service]),
):
    service_response = finduser_service.finduser(token)
    return ResponseDto(message = "User Detail find successsfully", status = 200, data=service_response)


       
