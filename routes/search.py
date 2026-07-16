from fastapi import APIRouter
from utils.db import db

router = APIRouter(prefix="/search")

@router.get("/users")
async def search_users(q: str):
    cursor = db["users"].find({"username": {"$regex": q, "$options": "i"}})
    return {"results": [u async for u in cursor]}

@router.get("/tournaments")
async def search_tournaments(q: str):
    cursor = db["tournaments"].find({"name": {"$regex": q, "$options": "i"}})
    return {"results": [
        {"id": str(t["_id"]), "name": t["name"]}
        async for t in cursor
    ]}
