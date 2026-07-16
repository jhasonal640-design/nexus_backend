from pydantic import BaseModel

class ChatMessage(BaseModel):
    to: str
    message: str
