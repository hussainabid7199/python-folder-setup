from abc import ABC, abstractmethod

from dtos.UploadDto import UploadDto
from models.UploadModel import UploadModel

from fastapi import UploadFile

class IUploadService(ABC):
    @abstractmethod
    async def upload(self, file: UploadFile, model: UploadModel) -> UploadDto:
        pass