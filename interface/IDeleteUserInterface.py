from abc import abstractmethod, ABC

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class IDeleteUserService(ABC):
    @abstractmethod
    def deleteuser(token: str = Depends(oauth2_scheme)):
        pass