from fastapi import APIRouter, Depends
from utils.auth_utils import get_token, get_user_from_token
from utils.db import db
from models.user_models import ProfileUpdate

router = APIRouter(prefix="/profile")

@router.get("/me")
async def get_me(token: str = Depends(get_token)):
    username = get_user_from_token(token)
    user = await db["users"].find_one({"username": username})

    return {
        "username": user["username"],
        "name": user.get("name", ""),
        "email": user.get("email", ""),
        "bio": user.get("bio", ""),
        "role": user.get("role", "user"),
        "friends": user.get("friends", []),
        "friend_requests": user.get("friend_requests", [])
    }

@router.post("/update")
async def update_me(data: ProfileUpdate, token: str = Depends(get_token)):
    username = get_user_from_token(token)

    update_data = {k: v for k, v in data.dict().items() if v is not None}
    await db["users"].update_one({"username": username}, {"$set": update_data})

    return {"message": "Profile updated"}
