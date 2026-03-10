import random

def speech_to_text(audio_file):
    """
    Stubs the Speech-to-Text conversion.
    In a production environment, this would use Whisper, Vosk, or Google Speech API.
    """
    # Mocking some possible outcomes for demo purposes
    mock_sentences = [
        "remind me to call John at 6 pm",
        "remind me to buy groceries in 10 minutes",
        "remind me to pick up kids at 4 30 pm",
        "remind me to start the meeting in 2 hours"
    ]
    
    # In this mock, we just return a random sentence or a default one
    return random.choice(mock_sentences)