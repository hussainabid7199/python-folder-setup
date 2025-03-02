from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from diInjector.diExtension import Container
from dtos.ResponseDto import ResponseDto
from dtos.ChatDto import ChatDto
from exceptions.CustomError import custom_error
from interface.IChatInterface import IChatService
from models.ChatModel import ChatModel

ChatRouter = APIRouter()

@ChatRouter.post("/chat", response_model=ResponseDto[ChatDto], status_code=200)
@inject
def chat(
    model: ChatModel,
    chat_service: IChatService = Depends(Provide[Container.chat_service]),
):
    try:
        input_text = model.query
        service_response = chat_service.chat(input_text)

        return ResponseDto(
            message="Start chatting", 
            status="success",
            statusCode=200,
            data=service_response
        )
    
    except Exception as e:
        return custom_error(e)