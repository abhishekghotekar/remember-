import os
import threading
import torch
import soundfile as sf
from datetime import datetime

# Lazy load Chatterbox (it's heavy)
_cb_instance = None
_cb_lock = threading.Lock()

def _get_cb():
    global _cb_instance
    with _cb_lock:
        if _cb_instance is None:
            try:
                from chatterbox import Chatterbox
                # Use CPU for server deployment
                _cb_instance = Chatterbox(device="cpu")
            except Exception as e:
                print(f"Failed to load Chatterbox: {e}")
                return None
    return _cb_instance

def speak_text(text: str):
    """
    Generates speech using Chatterbox TTS and saves it (or plays it if device exists).
    On servers (Render), this can save the audio to static files for the frontend.
    """
    def run_tts():
        cb = _get_cb()
        if not cb:
            print("Chatterbox not available.")
            return

        try:
            print(f"Generating speech: {text}")
            waveform = cb.say(text)
            
            # Ensure static directory exists
            static_dir = os.path.join(os.getcwd(), "static", "audio")
            os.makedirs(static_dir, exist_ok=True)
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tts_{timestamp}.wav"
            filepath = os.path.join(static_dir, filename)
            
            # Waveform to file (depends on how cb.say() returns. Typically a torch tensor)
            # If it's a tensor, we need to convert to numpy.
            if hasattr(waveform, "cpu"):
                data = waveform.cpu().numpy()
            else:
                data = waveform
                
            sf.write(filepath, data, 22050) # Assuming 22.05kHz as standard for many TTS
            print(f"Speech saved to {filepath}")
            
            # On local machines (Windows), we could try to play it
            if os.name == 'nt':
                try:
                    import winsound
                    winsound.PlaySound(filepath, winsound.SND_FILENAME)
                except:
                    pass
        except Exception as e:
            print(f"TTS Error: {e}")

    threading.Thread(target=run_tts, daemon=True).start()
