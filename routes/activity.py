from fastapi import APIRouter, Depends
from utils.db import db
from utils.auth_utils import get_token, get_user_from_token

router = APIRouter(prefix="/activity")

@router.get("/my")
async def my_activity(token: str = Depends(get_token)):
    username = get_user_from_token(token)

    cursor = db["activity"].find({"username": username}).sort("timestamp", -1)
    return {"activity": [a async for a in cursor]}

@router.get("/global")
async def global_activity():
    cursor = db["activity"].find().sort("timestamp", -1)
    return {"activity": [a async for a in cursor]}
