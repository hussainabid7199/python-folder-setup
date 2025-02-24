from fastapi import APIRouter, BackgroundTasks, Depends
from dependency_injector.wiring import inject, Provide
from dtos.UserDto import UserDto
from interface.IAccountInterface import IAccountService
from diInjector.diExtension import Container
from models.LoginModel import LoginModel
from models.RegisterModel import RegisterModel
from dtos.ResponseDto import ListResponseDto, ResponseDto

router = APIRouter()


@router.post("/register", response_model=ResponseDto[UserDto])
@inject
def register(
    model: RegisterModel,
    background_tasks : BackgroundTasks,
    account_service: IAccountService = Depends(Provide[Container.account_service]),
):
    service_response = account_service.register(model, background_tasks)
    return ResponseDto(
        message="User registered successfully", status=200, data=service_response
    )


@router.post("/login", response_model=ResponseDto[UserDto])
@inject
def login(
    model: LoginModel,
    account_service: IAccountService = Depends(Provide[Container.account_service]),
):
    response = account_service.login(model)
    if response is None:
        return {"message": "Unauthorize", "status": 401, "data": {}}
    return {"message": "Success", "status": 200, "data": response}


@router.get("/ping", response_model=ResponseDto[ListResponseDto[UserDto]])
def ping():
    return {
        "message": "Pong!",
        "status": 200,
        "data": {
            "totalRecord": 2,
            "data": [
                {
                    "id": "1",
                    "name": "harsh",
                    "email": "harsh@example.com",
                    "password": "harsh@example.com",
                },
                {
                    "id": "2",
                    "name": "john",
                    "email": "john@example.com",
                    "password": "john@example.com",
                },
            ],
        },
    }
