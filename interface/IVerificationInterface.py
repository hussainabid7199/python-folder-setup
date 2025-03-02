from abc import ABC, abstractmethod

from dtos.VerificationDto import VerificationDto
from models.VerificationModel import VerificationModel

class IVerificationService(ABC):
    @abstractmethod
    def verify(self, model: VerificationModel) -> VerificationDto:
        pass