from fastapi import APIRouter, Depends, HTTPException
from utils.db import db
from utils.auth_utils import get_token, get_user_from_token
from models.chat_models import ChatMessage
import time

router = APIRouter(prefix="/chat")

@router.post("/send")
async def send_message(data: ChatMessage, token: str = Depends(get_token)):
    sender = get_user_from_token(token)

    if sender == data.to:
        raise HTTPException(status_code=400, detail="Cannot message yourself")

    receiver = await db["users"].find_one({"username": data.to})
    if not receiver:
        raise HTTPException(status_code=404, detail="User not found")

    msg = {
        "from": sender,
        "to": data.to,
        "message": data.message,
        "timestamp": time.time()
    }

    await db["messages"].insert_one(msg)

    await db["notifications"].insert_one({
        "to": data.to,
        "from": sender,
        "message": f"New message from {sender}",
        "timestamp": time.time(),
        "seen": False
    })

    return {"message": "Message sent"}

@router.get("/history/{other}")
async def history(other: str, token: str = Depends(get_token)):
    username = get_user_from_token(token)

    cursor = db["messages"].find({
        "$or": [
            {"from": username, "to": other},
            {"from": other, "to": username}
        ]
    }).sort("timestamp", 1)

    return {"history": [m async for m in cursor]}

@router.get("/inbox")
async def inbox(token: str = Depends(get_token)):
    username = get_user_from_token(token)

    cursor = db["messages"].find({
        "$or": [{"from": username}, {"to": username}]
    }).sort("timestamp", -1)

    inbox = {}
    async for m in cursor:
        other = m["to"] if m["from"] == username else m["from"]
        if other not in inbox:
            inbox[other] = {
                "last_message": m["message"],
                "timestamp": m["timestamp"]
            }

    return {"inbox": inbox}
