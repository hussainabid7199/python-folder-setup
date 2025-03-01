from abc import ABC, abstractmethod

from dtos.UploadDto import UploadDto
from models.UploadModel import UploadModel

from fastapi import UploadFile

class IUploadService(ABC):
    @abstractmethod
    # def upload(self, model: UploadModel) -> UploadDto:
    #     pass
    async def upload(self, file: UploadFile, model: UploadModel) -> UploadDto:
        pass