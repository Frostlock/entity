"""
Text to speech & Audio playback
"""
from gtts import gTTS
from time import sleep
import tempfile
import pygame

pygame.mixer.init()

# def CreateMp3(text):
#     tts = gTTS(text=text, lang='en')
#     f = open(SPEECHDIR + text + ".mp3", "w")
#     tts.write_to_fp(f)
#     f.close()
# '''
# CreateMp3("No")
# CreateMp3("Goodbye")
# CreateMp3("Good morning")
# CreateMp3("Good afternoon")
# CreateMp3("Good evening")
# CreateMp3("System online and fully operational")
# CreateMp3("You're welcome.")
# CreateMp3("No problem.")
# CreateMp3("My pleasure.")
# '''

def play_mp3(filenameorobject):
    # See example here to tie into pygame music end event
    # http://www.python-forum.org/viewtopic.php?f=26&t=9948
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.queue(filenameorobject)
    else:
        pygame.mixer.music.load(filenameorobject)
        pygame.mixer.music.play()

def beep():
    play_mp3("./components/beep.mp3")

def speak(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    f = tempfile.SpooledTemporaryFile()
    tts.write_to_fp(f)
    f.seek(0)
    play_mp3(f)
    while pygame.mixer.music.get_busy():
        sleep(1)
    f.close()

if __name__ == "__main__":
    speak("Test, test, test", lang='nl')