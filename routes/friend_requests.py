from fastapi import APIRouter, Depends, HTTPException
from utils.db import db
from utils.auth_utils import get_token, get_user_from_token
from models.friend_models import FriendRequest, FriendDecision
import time

router = APIRouter(prefix="/friend_requests")

@router.post("/send")
async def send_request(data: FriendRequest, token: str = Depends(get_token)):
    sender = get_user_from_token(token)

    if sender == data.to:
        raise HTTPException(status_code=400, detail="Cannot send to yourself")

    receiver = await db["users"].find_one({"username": data.to})
    if not receiver:
        raise HTTPException(status_code=404, detail="User not found")

    if sender in receiver.get("friends", []):
        return {"message": "Already friends"}

    if sender in receiver.get("friend_requests", []):
        return {"message": "Already requested"}

    await db["users"].update_one(
        {"username": data.to},
        {"$addToSet": {"friend_requests": sender}}
    )

    await db["notifications"].insert_one({
        "to": data.to,
        "from": sender,
        "message": f"{sender} sent you a friend request",
        "timestamp": time.time(),
        "seen": False
    })

    return {"message": "Request sent"}

@router.get("/my")
async def my_requests(token: str = Depends(get_token)):
    username = get_user_from_token(token)
    user = await db["users"].find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"requests": user.get("friend_requests", [])}

@router.post("/accept")
async def accept_request(data: FriendDecision, token: str = Depends(get_token)):
    username = get_user_from_token(token)

    user = await db["users"].find_one({"username": username})
    if not user or data.from_user not in user.get("friend_requests", []):
        raise HTTPException(status_code=404, detail="No such request")

    await db["users"].update_one(
        {"username": username},
        {"$pull": {"friend_requests": data.from_user}}
    )

    await db["users"].update_one(
        {"username": username},
        {"$addToSet": {"friends": data.from_user}}
    )

    await db["users"].update_one(
        {"username": data.from_user},
        {"$addToSet": {"friends": username}}
    )

    return {"message": "Accepted"}

@router.post("/reject")
async def reject_request(data: FriendDecision, token: str = Depends(get_token)):
    username = get_user_from_token(token)

    await db["users"].update_one(
        {"username": username},
        {"$pull": {"friend_requests": data.from_user}}
    )

    return {"message": "Rejected"}
