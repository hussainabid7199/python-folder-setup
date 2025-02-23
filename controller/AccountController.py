from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from dtos.UserDto import UserDto
from interface.IAccountInterface import IAccountService
from diInjector.diExtension import Container
from models.RegisterModel import RegisterModel
from dtos.ResponseDto import ListResponseDto, ResponseDto

router = APIRouter()

@router.post("/register", response_model=ResponseDto[UserDto])
@inject
def register(
    user_data: RegisterModel, 
    account_service: IAccountService = Depends(Provide[Container.account_service])
):
    service_response = account_service.register(user_data)
    return ResponseDto(
        message="User registered successfully",
        status=200,
        data=service_response
    )

@router.post("/login", response_model=ResponseDto[UserDto])
@inject
def login(
    credentials: dict, 
    account_service: IAccountService = Depends(Provide[Container.account_service])
):
    return account_service.login(credentials)


@router.get("/ping", response_model=ResponseDto[ListResponseDto[UserDto]])       
def ping():
    return {
        "message": "Pong!",
        "status": 200,
        "data": [
            
            {"id": "1", "name": "harsh", "email": "harsh@example.com", "password": "harsh@example.com"}
            ,{"id": "1", "name": "harsh", "email": "harsh@example.com", "password": "harsh@example.com"}]
    }
    