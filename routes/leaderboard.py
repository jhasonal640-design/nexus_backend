from fastapi import APIRouter, Depends
from utils.db import db
from utils.auth_utils import get_token, get_user_from_token
from models.user_models import ScoreUpdate

router = APIRouter(prefix="/leaderboard")

@router.post("/add")
async def add_score(data: ScoreUpdate, token: str = Depends(get_token)):
    username = get_user_from_token(token)

    await db["leaderboard"].update_one(
        {"username": username},
        {"$set": {"score": data.score}},
        upsert=True
    )

    return {"message": "Score updated"}

@router.get("/top")
async def top_players():
    cursor = db["leaderboard"].find().sort("score", -1).limit(10)
    return {"top": [p async for p in cursor]}

@router.get("/me")
async def my_rank(token: str = Depends(get_token)):
    username = get_user_from_token(token)

    user_score = await db["leaderboard"].find_one({"username": username})
    if not user_score:
        return {"message": "No score found"}

    cursor = db["leaderboard"].find().sort("score", -1)
    rank = 1

    async for p in cursor:
        if p["username"] == username:
            break
        rank += 1

    return {"username": username, "score": user_score["score"], "rank": rank}
