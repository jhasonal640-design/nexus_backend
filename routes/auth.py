from fastapi import APIRouter, HTTPException, Depends
from utils.db import db
from utils.hashing import hash_pw, verify_pw
from utils.jwt_utils import make_token
from models.user_models import Register, Login

router = APIRouter(prefix="/auth")

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

@router.post("/login")
async def login(data: Login):
    user = await db["users"].find_one({"username": data.username})
    if not user:
        return {"error": "User not found"}

    if not verify_pw(data.password, user["password"]):
        return {"error": "Wrong password"}

    token = make_token(data.username)
    return {"message": "Login successful", "token": token}
