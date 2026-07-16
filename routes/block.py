from fastapi import APIRouter, Depends
from utils.db import db
from utils.auth_utils import get_token, get_user_from_token

router = APIRouter(prefix="/block")

@router.post("/add/{user}")
async def block_user(user: str, token: str = Depends(get_token)):
    username = get_user_from_token(token)

    await db["users"].update_one(
        {"username": username},
        {"$addToSet": {"blocked": user}}
    )

    return {"message": f"{user} blocked"}

@router.post("/remove/{user}")
async def unblock_user(user: str, token: str = Depends(get_token)):
    username = get_user_from_token(token)

    await db["users"].update_one(
        {"username": username},
        {"$pull": {"blocked": user}}
    )

    return {"message": f"{user} unblocked"}

@router.get("/list")
async def list_blocked(token: str = Depends(get_token)):
    username = get_user_from_token(token)
    user = await db["users"].find_one({"username": username})
    return {"blocked": user.get("blocked", [])}
