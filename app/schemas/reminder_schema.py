from pydantic import BaseModel

class ReminderCreate(BaseModel):
    task: str
    time: str