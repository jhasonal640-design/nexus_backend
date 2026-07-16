from fastapi import APIRouter, Depends
from models.notifications_models import Notify
from utils.db import db
from utils.auth_utils import get_token, get_user_from_token
from models.notifications_models import Notify
import time

router = APIRouter(prefix="/notify")

@router.post("/send")
async def send_notification(data: Notify, token: str = Depends(get_token)):
    sender = get_user_from_token(token)

    await db["notifications"].insert_one({
        "to": data.to,
        "from": sender,
        "message": data.message,
        "timestamp": time.time(),
        "seen": False
    })

    return {"message": "Notification sent"}

@router.get("/my")
async def my_notifications(token: str = Depends(get_token)):
    username = get_user_from_token(token)

    cursor = db["notifications"].find({"to": username}).sort("timestamp", -1)
    return {"notifications": [n async for n in cursor]}

@router.delete("/clear")
async def clear_notifications(token: str = Depends(get_token)):
    username = get_user_from_token(token)

    await db["notifications"].delete_many({"to": username})
    return {"message": "Cleared"}
