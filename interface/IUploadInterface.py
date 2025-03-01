from abc import ABC, abstractmethod
from fastapi import File, UploadFile
from dtos.UploadDto import UploadDto


class IUploadService(ABC):
    @abstractmethod
    def upload(self, file: UploadFile = File(...)) -> dict:
        pass