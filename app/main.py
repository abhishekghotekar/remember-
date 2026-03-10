from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_reminder import router as reminder_router
from app.api.routes_voice import router as voice_router
from app.api.routes_user import router as user_router

app = FastAPI(title="Voice Reminder API", version="1.0.0")

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(reminder_router, prefix="/api", tags=["Reminders"])
app.include_router(voice_router, prefix="/api", tags=["Voice"])
app.include_router(user_router, prefix="/api", tags=["User"])

@app.get("/")
def home():
    return {
        "status": "ready",
        "service": "Voice Reminder Backend",
        "docs": "/docs"
    }