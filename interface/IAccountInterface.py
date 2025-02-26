from abc import ABC, abstractmethod
from typing import Dict

from fastapi import BackgroundTasks
from dtos.ResponseDto import ResponseDto
from dtos.UserDto import UserDto
from models.RegisterModel import RegisterModel


class IAccountService(ABC):
    @abstractmethod
    def register(self, model: RegisterModel) -> UserDto:
        pass

    @abstractmethod
    def login(self, credentials: Dict) -> Dict:
        pass
