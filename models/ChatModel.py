from pydantic import BaseModel

class ChatModel(BaseModel):
    query: str