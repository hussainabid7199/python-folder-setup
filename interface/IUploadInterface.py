from abc import ABC, abstractmethod

from dtos.UploadDto import UploadDto
from models.UploadModel import UploadModel

class IUploadService(ABC):
    @abstractmethod
    def upload(self, model: UploadModel) -> UploadDto:
        pass