from fastapi import APIRouter, HTTPException
from app.schemas.reminder_schema import ReminderCreate
from app.services.reminder_service import create_reminder, get_reminders, delete_reminder

router = APIRouter()

@router.post("/reminder")
def add_reminder(reminder: ReminderCreate):
    return create_reminder(reminder)

@router.get("/reminders")
def list_reminders():
    return get_reminders()

@router.delete("/reminder/{reminder_id}")
def remove_reminder(reminder_id: str):
    return delete_reminder(reminder_id)