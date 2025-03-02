from abc import ABC, abstractmethod

from dtos.ChatDto import ChatDto
from models.ChatModel import ChatModel

class IChatService(ABC):
    @abstractmethod
    def chat(self, model: ChatModel) -> ChatDto:
        pass