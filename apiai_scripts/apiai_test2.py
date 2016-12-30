try:
    import pyaudio
except ImportError:
    raise AttributeError("Could not find PyAudio; check installation")
from distutils.version import LooseVersion

if LooseVersion(pyaudio.__version__) < LooseVersion("0.2.9"):
    raise AttributeError("PyAudio 0.2.9 or later is required (found version {0})".format(pyaudio.__version__))

import speech_recognition
import pyttsx

speech_engine = pyttsx.init('espeak')
speech_engine.setProperty('rate', 150)


def speak(text):
    speech_engine.say(text)
    speech_engine.runAndWait()

recognizer = speech_recognition.Recognizer()


def listen():
    with speech_recognition.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            return recognizer.recognize_sphinx(audio)
        except speech_recognition.UnknownValueError:
            print("Could not understand audio")
        except speech_recognition.RequestError as e:
            print("Recog Error; {0}".format(e))

        return ""


speak("Say something!")
speak("I heard you say " + listen())
