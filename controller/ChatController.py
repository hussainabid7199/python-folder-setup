from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from diInjector.diExtension import Container
from dtos.ResponseDto import ResponseDto
from dtos.ChatDto import ChatDto
from interface.IChatInterface import IChatService
from models.ChatModel import ChatModel

ChatRouter = APIRouter()

@ChatRouter.post("/chat", response_model=ResponseDto[ChatDto])
@inject
def chat(
    model: ChatModel,
    chat_service: IChatService = Depends(Provide[Container.chat_service]),
):
    service_response = chat_service.chat(model)
    return ResponseDto(
        message="start chating", status=200, data=service_response
    )
