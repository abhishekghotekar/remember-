import uvicorn
import os

if __name__ == "__main__":
    # Ensure the app can find the 'backend' folder if needed, 
    # but running from this directory is standard.
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
