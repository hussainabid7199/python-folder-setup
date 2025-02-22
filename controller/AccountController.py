from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from interface.IAccountInterface import IAccountService
from diInjector.diExtension import Container 

router = APIRouter()

@router.post("/register")
@inject
def register(
    user_data: dict, 
    account_service: IAccountService = Depends(Provide[Container.account_service])
):
    return account_service.register(user_data)

@router.post("/login")
@inject
def login(
    credentials: dict, 
    account_service: IAccountService = Depends(Provide[Container.account_service])
):
    return account_service.login(credentials)
