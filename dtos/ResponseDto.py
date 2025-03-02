from typing import Generic, List, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class ResponseDto(BaseModel, Generic[T]):
    message: str;
    status: str;
    statusCode: int
    data: Optional[T] = None;

class ListResponseDto(BaseModel, Generic[T]):
    totalRecord: int;
    data: Optional[List[T]] = None;
