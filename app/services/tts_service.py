import pyttsx3
import threading

def speak_text(text: str):
    """
    Runs pyttsx3 in a separate thread to avoid blocking the main FastAPI loop.
    """
    def run_engine():
        try:
            # Fix for Windows threading (SAPI5)
            try:
                import pythoncom
                pythoncom.CoInitialize()
            except ImportError:
                pass

            # Initialize engine in the thread
            engine = pyttsx3.init()

            engine.setProperty('rate', 150)  # Speed percent (can be 100-200)
            engine.setProperty('volume', 0.9) # Volume 0-1
            
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"TTS Error: {e}")

    threading.Thread(target=run_engine, daemon=True).start()
