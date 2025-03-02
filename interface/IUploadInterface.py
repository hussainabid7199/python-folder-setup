from abc import ABC, abstractmethod
from fastapi import File, UploadFile
from dtos.UploadDto import UploadDto
from models.UploadModel import UploadModel

class IUploadService(ABC):
    @abstractmethod
    async def upload(self, file: UploadFile, model: UploadModel) -> UploadDto:
        pass