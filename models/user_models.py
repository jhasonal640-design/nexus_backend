from pydantic import BaseModel

class Register(BaseModel):
    username: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class ProfileUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    bio: str | None = None

# ⭐ MISSING MODELS (add these)
class ScoreUpdate(BaseModel):
    score: int

class MatchRecord(BaseModel):
    opponent: str
    score: int
    result: str
