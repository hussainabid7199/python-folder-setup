from pydantic import BaseModel

class ChatDto(BaseModel):
    id: str;
    output: str;