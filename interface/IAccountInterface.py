from abc import ABC, abstractmethod
from typing import Dict

class IAccountService(ABC):
    @abstractmethod
    def register(self, user_data: Dict) -> Dict:
        pass

    @abstractmethod
    def login(self, credentials: Dict) -> Dict:
        pass
