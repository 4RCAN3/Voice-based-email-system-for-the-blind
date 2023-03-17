import pyttsx3
from dotenv import load_dotenv


def voice(settings: dict) -> object:

    load_dotenv()
    engine = pyttsx3.init()
    engine.setProperty('rate', int(settings['rate']))
    engine.setProperty('volume', float(settings['volume']))

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[int(settings['voice'])])

    return engine