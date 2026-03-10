from fastapi import APIRouter

router = APIRouter()

@router.get("/profile")
def get_profile():
    return {
        "username": "User",
        "preferences": {
            "voice": "default",
            "language": "en-US"
        }
    }
