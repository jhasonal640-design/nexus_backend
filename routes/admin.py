from fastapi import APIRouter, Depends, HTTPException
from utils.db import db
from utils.auth_utils import get_token, get_user_from_token

router = APIRouter(prefix="/admin")

@router.get("/stats")
async def stats(token: str = Depends(get_token)):
    username = get_user_from_token(token)

    user = await db["users"].find_one({"username": username})
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not admin")

    total_users = await db["users"].count_documents({})
    total_messages = await db["messages"].count_documents({})
    total_tournaments = await db["tournaments"].count_documents({})
    total_matches = await db["match_history"].count_documents({})

    return {
        "total_users": total_users,
        "total_messages": total_messages,
        "total_tournaments": total_tournaments,
        "total_matches": total_matches
    }
