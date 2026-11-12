from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ROUTES IMPORT
from routes.auth import router as auth_router
from routes.profile import router as profile_router
from routes.leaderboard import router as leaderboard_router
from routes.matches import router as matches_router
from routes.friends import router as friends_router
from routes.friend_requests import router as friend_requests_router
from routes.chat import router as chat_router
from routes.notifications import router as notifications_router
from routes.tournaments import router as tournaments_router
from routes.badges import router as badges_router
from routes.activity import router as activity_router
from routes.search import router as search_router
from routes.block import router as block_router
from routes.admin import router as admin_router

app = FastAPI(
    title="Nexus Gaming Platform API",
    description="Full Social + Gaming + Tournament Backend",
    version="1.0.0"
)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],  # Or use ["*"] while testing locally
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# HOME
@app.get("/")
def home():
    return {"message": "Nexus Backend Running Successfully"}

# REGISTER ROUTES
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(leaderboard_router)
app.include_router(matches_router)
app.include_router(friends_router)
app.include_router(friend_requests_router)
app.include_router(chat_router)
app.include_router(notifications_router)
app.include_router(tournaments_router)
app.include_router(badges_router)
app.include_router(activity_router)
app.include_router(search_router)
app.include_router(block_router)
app.include_router(admin_router)
