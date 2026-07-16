from fastapi import APIRouter, Depends, HTTPException
from utils.db import db
from utils.auth_utils import get_token, get_user_from_token
from models.tournament_models import TournamentCreate, TournamentJoin, TournamentScore
from bson import ObjectId
import time

router = APIRouter(prefix="/tournament")

@router.post("/create")
async def create_tournament(data: TournamentCreate, token: str = Depends(get_token)):
    username = get_user_from_token(token)

    tournament = {
        "name": data.name,
        "created_by": username,
        "players": [username],
        "scores": {},
        "status": "ongoing",
        "timestamp": time.time()
    }

    res = await db["tournaments"].insert_one(tournament)
    return {"message": "Tournament created", "id": str(res.inserted_id)}

@router.post("/join")
async def join_tournament(data: TournamentJoin, token: str = Depends(get_token)):
    username = get_user_from_token(token)

    try:
        tid = ObjectId(data.tournament_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid tournament id")

    tournament = await db["tournaments"].find_one({"_id": tid})
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")

    await db["tournaments"].update_one(
        {"_id": tid},
        {"$addToSet": {"players": username}}
    )

    return {"message": "Joined tournament"}

@router.post("/score")
async def submit_score(data: TournamentScore, token: str = Depends(get_token)):
    username = get_user_from_token(token)

    try:
        tid = ObjectId(data.tournament_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid tournament id")

    await db["tournaments"].update_one(
        {"_id": tid},
        {"$set": {f"scores.{username}": data.score}}
    )

    return {"message": "Score submitted"}

@router.get("/leaderboard/{tid}")
async def tournament_leaderboard(tid: str):
    try:
        tid_obj = ObjectId(tid)
    except:
        raise HTTPException(status_code=400, detail="Invalid tournament id")

    t = await db["tournaments"].find_one({"_id": tid})
    if not t:
        raise HTTPException(status_code=404, detail="Tournament not found")

    scores = t.get("scores", {})
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return {"leaderboard": [{"username": u, "score": s} for u, s in sorted_scores]}

@router.get("/list")
async def list_tournaments():
    cursor = db["tournaments"].find().sort("timestamp", -1)
    return {"tournaments": [
        {
            "id": str(t["_id"]),
            "name": t["name"],
            "players": t.get("players", []),
            "status": t.get("status", "ongoing")
        }
        async for t in cursor
    ]}
