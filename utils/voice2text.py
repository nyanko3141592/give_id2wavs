import speech_recognition as sr

r = sr.Recognizer()

def v2t(path:str) -> str:
    with sr.AudioFile(path) as source:
        audio = r.record(source)
    return r.recognize_google(audio, language='ja-JP')