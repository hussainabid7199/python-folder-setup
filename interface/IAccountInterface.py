from abc import ABC, abstractmethod
from typing import Dict

from dtos.RegisterDto import RegisterDto

class IAccountService(ABC):
    @abstractmethod
    def register(self, user_data: RegisterDto) -> Dict:
        pass

    @abstractmethod
    def login(self, credentials: Dict) -> Dict:
        pass
