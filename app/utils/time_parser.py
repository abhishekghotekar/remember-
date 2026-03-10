import re
import datetime

def parse_command(text):
    """
    Parses text to extract task and time.
    Supports:
    - "remind me to [task] at [time]"
    - "remind me to [task] in [X] minutes"
    - "[task] at [time]"
    """
    text = text.lower().strip()
    
    # Remove prefix
    text = re.sub(r"^(remind me to|remind me|remind)\s+", "", text)
    
    # 1. Check for relative time "in X minutes/hours"
    rel_match = re.search(r"(.+?)\s+in\s+(\d+)\s+(minute|min|minutes|hour|hours)", text)
    if rel_match:
        task = rel_match.group(1).strip()
        value = int(rel_match.group(2))
        unit = rel_match.group(3)
        
        now = datetime.datetime.now()
        if "hour" in unit:
            scheduled_time = now + datetime.timedelta(hours=value)
        else:
            scheduled_time = now + datetime.timedelta(minutes=value)
            
        return {
            "task": task,
            "time": scheduled_time.strftime("%H:%M"),
            "full_date": scheduled_time.isoformat()
        }

    # 2. Check for absolute time "at 5 pm", "at 17:30"
    abs_match = re.search(r"(.+?)\s+at\s+(\d+)(?::(\d+))?\s*(am|pm)?", text)
    if abs_match:
        task = abs_match.group(1).strip()
        hour = int(abs_match.group(2))
        minute = int(abs_match.group(3)) if abs_match.group(3) else 0
        ampm = abs_match.group(4)
        
        if ampm == "pm" and hour < 12:
            hour += 12
        elif ampm == "am" and hour == 12:
            hour = 0
            
        scheduled_time = datetime.datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # If the time has already passed today, assume tomorrow
        if scheduled_time < datetime.datetime.now():
            scheduled_time += datetime.timedelta(days=1)
            
        return {
            "task": task,
            "time": scheduled_time.strftime("%H:%M"),
            "full_date": scheduled_time.isoformat()
        }

    return {
        "task": text,
        "time": "unknown",
        "full_date": None
    }