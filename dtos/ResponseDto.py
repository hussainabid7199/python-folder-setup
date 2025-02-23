from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class ResponseDto(BaseModel, Generic[T]):
    message: str
    status: int
    data: Optional[T] = None

class ListResponseDto(BaseModel, Generic[T]):
    totalRecord: int
    data: Optional[T] = None
