from fastapi import Header, HTTPException
from utils.jwt_utils import decode_token

def get_token(auth: str = Header(None, convert_underscores=False)):
    if auth is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization format")
    return auth.split(" ")[1]

def get_user_from_token(token):
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username
