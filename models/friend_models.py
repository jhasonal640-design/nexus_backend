from pydantic import BaseModel

class FriendAction(BaseModel):
    friend: str

class FriendRequest(BaseModel):
    to: str

class FriendDecision(BaseModel):
    from_user: str
