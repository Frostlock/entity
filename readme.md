# Introduction
This is an experiment in creating a personal assistant, an entity :)  
The entity has a command line interface and a voice interface. This was mainly 
an experiment for me to get some experience with speech recognition and text to speech.

**Python 3**  
I thought it was about time for me to start using Python 3. I can't be bothered to keep 
this compatible with Python 2.7 :) That being said, most of it should work under 
Python 2.7 as well.

# Installation
I am running this project on a Raspberry Pi 3 Model B.
The instructions below should also work on a regular linux distribution.

### 1. Install Raspbian
I'm using Raspbian Stretch (based on an image from September 2017).

### 2. Install dependancies

**Voice recognition**  
speech_recognition  
sudo pip3 install SpeechRecognition --upgrade  
This package also requires flac which is not installed by default on in Raspbian.  
sudo apt-get install flac  

**PyAudio**  
Attention: Speech recognition requires a recent version    
pip3 gave a build error on my raspberry:    
sudo pip3 install PyAudio --upgrade  
Easy way around this, install it from the repositories:  
sudo apt-get install python3-pyaudio

**Text to speech**  
gTTS  
sudo pip3 install gTTS --upgrade

**GUI and audio output**  
pygame  
sudo pip3 install pygame --upgrade  
The added advantage of pygame is that it allows me to run a graphical GUI without 
running an X server.

**Natural Language Processing**  
textblob  
Using textblob at the moment, might investigate using google instead.  
https://textblob.readthedocs.io/en/dev/install.html#installing-upgrading-from-the-pypi

**Google APIs**  
google-api-python-client  
sudo pip3 install google-api-python-client --upgrade


### 3. Configuration of the Microphone
I'm using an USB microphone and speaker combination on my raspberry. The easiest 
set of instructions I have found are from knight-of-pi:  
http://www.knight-of-pi.org/raspberry-pi-enable-an-usb-sound-card-for-Raspbian-jessie/

### 4. Optional: Configuration of the display
I use the official Raspberry Pi 7 inch touchscreen with a case. In the case the 
display output is upside down. To rotate the display and the touch coordinates, 
open /boot/config.txt in your favourite editor and add the line:  
lcd_rotate=2  
Note: Don't use the documented display_rotate, it performs a performance expensive 
rotation of the screen and does not rotate the touch input.
More information about the display can be found here:  
http://forums.pimoroni.com/t/official-7-raspberry-pi-touch-screen-faq/959

# Troubleshooting

**Audio related error messages**  
At startup there is a bunch of alsa related error messages. These don't appear to cause 
any issue but at some point I need to look into these :)


# TODO / Feature enhancements

##### Implement entity states  
Idea is to make the entity more aware of the current context enhancing precision of answers and creating greater sense of personality. 

##### Fake emotions  
Emotions would be fun too, for example entity getting annoyed after same questions, bored after silence, apologetic after not understanding several instructions in a row.

##### Use Google speech API directly instead of through the extra gTTS module?**