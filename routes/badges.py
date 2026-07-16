from fastapi import APIRouter, Depends
from utils.db import db
from utils.auth_utils import get_token, get_user_from_token
import time

router = APIRouter(prefix="/badges")

@router.get("/my")
async def my_badges(token: str = Depends(get_token)):
    username = get_user_from_token(token)
    user = await db["users"].find_one({"username": username})
    return {"badges": user.get("badges", [])}

@router.post("/grant/{badge}")
async def grant_badge(badge: str, token: str = Depends(get_token)):
    username = get_user_from_token(token)

    await db["users"].update_one(
        {"username": username},
        {"$addToSet": {"badges": badge}}
    )

    await db["activity"].insert_one({
        "username": username,
        "action": f"Unlocked badge: {badge}",
        "timestamp": time.time()
    })

    return {"message": f"Badge '{badge}' granted"}

@router.get("/list")
async def list_badges():
    return {
        "available_badges": [
            "Champion",
            "Top Scorer",
            "Fast Player",
            "Friendly",
            "Legend",
            "Tournament Winner"
        ]
    }
