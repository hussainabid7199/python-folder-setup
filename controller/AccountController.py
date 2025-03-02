from fastapi import APIRouter, BackgroundTasks, Depends
from dependency_injector.wiring import inject, Provide
from dtos.UserDto import UserDto
from exceptions.CustomError import custom_error
from interface.IAccountInterface import IAccountService
from diInjector.diExtension import Container
from models.LoginModel import LoginModel
from models.RegisterModel import RegisterModel
from dtos.ResponseDto import ListResponseDto, ResponseDto

accountRouter = APIRouter()


@accountRouter.post("/register", response_model=ResponseDto[UserDto], status_code=201)
@inject
def register(
    model: RegisterModel,
    account_service: IAccountService = Depends(Provide[Container.account_service]),
):
    try:
        service_response = account_service.register(model)
        return ResponseDto(
            message="User registered successfully",
            status="success",
            statusCode=201,
            data=service_response,
        )
    except Exception as e:
        return custom_error(e)


@accountRouter.post("/login", response_model=ResponseDto[UserDto], status_code=201)
@inject
def login(
    model: LoginModel,
    account_service: IAccountService = Depends(Provide[Container.account_service]),
):
    try:
        response = account_service.login(model)
        if response is None:
            return ResponseDto(
                message="Unauthorized", 
                status="failed", 
                statusCode=401, 
                data=None
            )
        return ResponseDto(
            message="Success", 
            status="success", 
            statusCode=201, 
            data=response
        )
    
    except Exception as e:
        return custom_error(e)


@accountRouter.get(
    "/ping", response_model=ResponseDto[ListResponseDto[UserDto]], status_code=200
)
def ping():
     try:
        return ResponseDto(
            message="Pong!", 
            status="success", 
            statusCode=200, 
            data=ListResponseDto(
                totalRecord=2,
                data= [
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
          )
        )
     except Exception as e:
        return custom_error(e)
