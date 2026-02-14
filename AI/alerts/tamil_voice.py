import pyttsx3

_engine = None

def tamil_voice_alert():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty("rate", 150)

    _engine.say("விவசாயிகளே கவனம். பயிர் அழுத்தம் கண்டறியப்பட்டுள்ளது")
    _engine.runAndWait()
