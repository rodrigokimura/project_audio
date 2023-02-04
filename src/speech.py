import os
from time import sleep

import pyttsx3
import vlc
from gtts import gTTS
from mutagen.mp3 import MP3


def offline_speech(text: str) -> None:
    pyttsx3.speak(text)


def online_speech(text: str) -> None:
    temp_file = "temp.mp3"
    gTTS(text=text, lang="en", slow=False).save(temp_file)
    vlc.MediaPlayer(temp_file).play()

    sleep(MP3(temp_file).info.length)
    os.remove(temp_file)


def speak(text: str):
    try:
        online_speech(text)
    except Exception:
        offline_speech(text)
