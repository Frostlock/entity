## Introduction
This is an experiment in creating a personal assistant, an entity :)  
The entity has a command line interface and a voice interface. This was mainly 
an experiment for me to get some experience with speech recognition and text to speech.

## Dependencies

**Prefer Python 3**  
I thought it was about time for me to start using Python 3. I can't be bothered to keep this compatible with Python 2.7 :) That being said, most of it should work under Python 2.7 as well.

**Voice recognition**  
speech_recognition  
sudo pip3 install SpeechRecognition --upgrade

**Text to speech**  
gTTS  
sudo pip3 install gTTS --upgrade

**Audio output**  
pygame  
sudo pip3 install pygame --upgrade

**Natural Language Processing**  
textblob
https://textblob.readthedocs.io/en/dev/install.html#installing-upgrading-from-the-pypi

**Google APIs**  
google-api-python-client  
sudo pip3 install google-api-python-client --upgrade

**PyAudio**  
should be installed by default but speech recognition requires latest version  
sudo pip3 install PyAudio --upgrade

## Troubleshooting

**Audio related error messages**  
I had some funky error messages and warnings showing up coming from pyaudio  
Minimal test to give these errors:  
python -c "import pyaudio;audio=pyaudio.PyAudio()"  
Solution: edit the alsa.conf file  
https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=136974


## TODO / Feature enhancements
**Implement entity states**  
Idea is to make the entity more aware of the current context enhancing precision of answers and creating greater sense of personality. 
**Fake emotions**  
Emotions would be fun too, for example entity getting annoyed after same questions, bored after silence, apologetic after not understanding several instructions in a row.
**Use Google speech API directly instead of through the extra modules**