import pyttsx3

engine = pyttsx3.init()
engine.say("Hello, I am your assistant!")
engine.runAndWait()



from gtts import gTTS
import os

tts = gTTS(text="Hello, I am your assistant!", lang='en')
tts.save("hello.mp3")
os.system("start hello.mp3")  # or use playsound