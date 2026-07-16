from typing import Optional

try:
    from pydantic import BaseModel  # type: ignore[import]
except Exception:  # fallback when pydantic is not installed (e.g., in type-checking/linter env)
    # Minimal BaseModel fallback to avoid import errors in editors/linters.
    # This does not provide pydantic validation; it's only a lightweight stand-in.
    class BaseModel:
        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)

        def dict(self):
            return self.__dict__.copy()

        def json(self):
            import json
            return json.dumps(self.dict())

class Register(BaseModel):
    username: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None

# ⭐ MISSING MODELS (add these)
class ScoreUpdate(BaseModel):
    score: int

class MatchRecord(BaseModel):
    opponent: str
    score: int
    result: str
