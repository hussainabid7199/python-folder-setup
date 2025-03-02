from abc import ABC, abstractmethod

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from dtos import FindUserDto

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class IFindUserService(ABC):
    @abstractmethod
    def finduser(self, token: str = Depends(oauth2_scheme)) -> FindUserDto:
        pass
