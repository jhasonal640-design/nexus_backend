from pydantic import BaseModel

class Notify(BaseModel):
    to: str
    message: str
