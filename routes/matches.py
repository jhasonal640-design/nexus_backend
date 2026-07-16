from fastapi import APIRouter, Depends
from utils.db import db
from utils.auth_utils import get_token, get_user_from_token
from models.user_models import MatchRecord
import time

router = APIRouter(prefix="/match")

@router.post("/add")
async def add_match(data: MatchRecord, token: str = Depends(get_token)):
    username = get_user_from_token(token)

    await db["match_history"].insert_one({
        "username": username,
        "opponent": data.opponent,
        "score": data.score,
        "result": data.result,
        "timestamp": time.time()
    })

    return {"message": "Match saved"}

@router.get("/my")
async def my_matches(token: str = Depends(get_token)):
    username = get_user_from_token(token)

    cursor = db["match_history"].find({"username": username}).sort("timestamp", -1)
    return {"matches": [m async for m in cursor]}
