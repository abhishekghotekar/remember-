from fastapi import APIRouter, UploadFile, File
from app.utils.time_parser import parse_command
from app.services.stt_service import speech_to_text
from app.services.tts_service import speak_text


router = APIRouter()

@router.post("/process-voice")
async def process_voice(file: UploadFile = File(...)):
    """
    Receives an audio file, converts it to text, and parses the command.
    """
    # In a real scenario, we'd save the file or process the stream
    # For now, we stub the STT service
    text = speech_to_text(file)
    parsed = parse_command(text)
    
    if parsed["time"] != "unknown":
        speak_text(f"Okay, I will remind you to {parsed['task']} at {parsed['time']}")
    
    return {
        "original_text": text,
        "parsed": parsed
    }

@router.post("/process-text")
def process_text(payload: dict):
    """
    Directly parse a text command (useful for testing or manual input).
    """
    text = payload.get("text", "")
    parsed = parse_command(text)

    if parsed["time"] != "unknown":
        speak_text(f"Reminder set for {parsed['task']} at {parsed['time']}")

    return {
        "original_text": text,
        "parsed": parsed
    }
