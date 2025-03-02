from pydantic import BaseModel
from typing import List

class UploadDto(BaseModel):
    file_name: str
    num_chunks: int
    file_id: str
    chunks: List[str]
