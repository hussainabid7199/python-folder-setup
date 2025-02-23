from abc import ABC, abstractmethod
from typing import Dict
from dtos.ResponseDto import ResponseDto
from dtos.UserDto import UserDto
from models.RegisterModel import RegisterModel


class IAccountService(ABC):
    @abstractmethod
    def register(self, user_data: RegisterModel) -> UserDto:
        pass

    @abstractmethod
    def login(self, credentials: Dict) -> Dict:
        pass
