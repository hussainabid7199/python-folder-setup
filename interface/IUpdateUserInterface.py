from abc import abstractmethod, ABC

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from dtos.UpdateUserDto import UpdateUserDto
from models.UpdateUserModel import UpdateUserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class IUpdateUserService(ABC):
    @abstractmethod
    def updateuser(
        self, model: UpdateUserModel, token: str = Depends(oauth2_scheme)
    ) -> UpdateUserDto:
        pass
