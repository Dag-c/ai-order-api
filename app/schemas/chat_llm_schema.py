from pydantic import BaseModel

class ChatLLM(BaseModel):
    intent: str
    data: dict = {}