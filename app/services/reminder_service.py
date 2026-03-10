import uuid
import threading
import time
import schedule
import re
from datetime import datetime
from app.services.tts_service import speak_text

# In-memory storage
reminders = []

def create_reminder(reminder_data):
    reminder = {
        "id": str(uuid.uuid4()),
        "task": reminder_data.task,
        "time": reminder_data.time,
        "created_at": datetime.now().isoformat(),
        "status": "pending"
    }
    reminders.append(reminder)
    
    # Schedule the actual alert (validate HH:MM format)
    if reminder["time"] and re.match(r"^\d{2}:\d{2}$", reminder["time"]):
        try:
            schedule.every().day.at(reminder["time"]).do(trigger_alert, reminder=reminder).tag(reminder["id"])
        except Exception as e:
            print(f"Error scheduling reminder: {e}")
    else:
        print(f"Invalid time format for reminder '{reminder['task']}': {reminder['time']}")
    
    return {
        "message": "Reminder created successfully",
        "data": reminder
    }

def trigger_alert(reminder):
    print(f"ALARM: {reminder['task']}")
    speak_text(f"Attention! This is your reminder to {reminder['task']}")
    
    # Update status to completed
    reminder["status"] = "completed"
    return schedule.CancelJob

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(10) # Check every 10 seconds

# Start background worker
threading.Thread(target=run_scheduler, daemon=True).start()

def get_reminders():
    return sorted(reminders, key=lambda x: x['time'])

def delete_reminder(reminder_id):
    global reminders
    reminders = [r for r in reminders if r['id'] != reminder_id]
    schedule.clear(reminder_id)
    return {"message": "Reminder deleted"}

def update_reminder_status(reminder_id, status):
    for r in reminders:
        if r['id'] == reminder_id:
            r['status'] = status
            return r
    return None
