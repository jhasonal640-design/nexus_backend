from fastapi import APIRouter, Depends, HTTPException, Header
from utils.db import db
from utils.hashing import hash_pw, verify_pw
from utils.jwt_utils import make_token, decode_token
from models.user_models import Register, Login

router = APIRouter(prefix="/auth")
@router.get("/me")
async def me(Authorization: str = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    parts = Authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = parts[1]
    payload = decode_token(token)
    username = None
    if isinstance(payload, dict):
        username = payload.get("username") or payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await db["users"].find_one({"username": username}, {"_id": 0, "password": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ---------------------------
# REGISTER
# ---------------------------
@router.post("/register")
async def register(data: Register):
    if await db["users"].find_one({"username": data.username}):
        return {"error": "User exists"}

    hashed = hash_pw(data.password)

    await db["users"].insert_one({
        "username": data.username,
        "password": hashed,
        "name": "",
        "email": "",
        "bio": "",
        "role": "user",
        "friends": [],
        "friend_requests": []
    })

    return {"message": "User registered"}

# ---------------------------
# LOGIN
# ---------------------------
@router.post("/login")
async def login(data: Login):
    user = await db["users"].find_one({"username": data.username})
    if not user:
        return {"error": "User not found"}

    if not verify_pw(data.password, user["password"]):
        return {"error": "Wrong password"}

    token = make_token(data.username)
    return {"message": "Login successful", "token": token}

# ---------------------------
# DELETE USER (MongoDB)
# ---------------------------
@router.delete("/delete/{username}")
async def delete_user(username: str):
    user = await db["users"].find_one({"username": username})
    if not user:
        return {"error": "User not found"}

    await db["users"].delete_one({"username": username})
    return {"message": f"User '{username}' deleted successfully"}
