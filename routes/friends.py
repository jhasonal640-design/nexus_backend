from fastapi import APIRouter, Depends, HTTPException
from utils.db import db
from utils.auth_utils import get_token, get_user_from_token
from models.friend_models import FriendAction

router = APIRouter(prefix="/friends")

@router.post("/add")
async def add_friend(data: FriendAction, token: str = Depends(get_token)):
    username = get_user_from_token(token)

    if username == data.friend:
        raise HTTPException(status_code=400, detail="Cannot add yourself")

    friend = await db["users"].find_one({"username": data.friend})
    if not friend:
        raise HTTPException(status_code=404, detail="User not found")

    await db["users"].update_one(
        {"username": username},
        {"$addToSet": {"friends": data.friend}}
    )

    return {"message": f"{data.friend} added"}

@router.post("/remove")
async def remove_friend(data: FriendAction, token: str = Depends(get_token)):
    username = get_user_from_token(token)

    await db["users"].update_one(
        {"username": username},
        {"$pull": {"friends": data.friend}}
    )

    return {"message": f"{data.friend} removed"}

@router.get("/list")
async def list_friends(token: str = Depends(get_token)):
    username = get_user_from_token(token)
    user = await db["users"].find_one({"username": username})
    return {"friends": user.get("friends", [])}

@router.get("/is_friend/{other}")
async def is_friend(other: str, token: str = Depends(get_token)):
    username = get_user_from_token(token)
    user = await db["users"].find_one({"username": username})
    return {"is_friend": other in user.get("friends", [])}
