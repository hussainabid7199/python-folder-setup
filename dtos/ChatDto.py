from pydantic import BaseModel

class ChatDto(BaseModel):
    # id: str;
    response: str;