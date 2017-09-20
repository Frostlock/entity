import components.ElizaTherapist as et

from actions import ActionLibrary

import components.TextToSpeech as tts
from components.VoiceRecognizer import VoiceRecognizer

from time import time
'''
import webbrowser
def WebSearch(searchText):
    tts.SpeakOnce("Searching Google for " + searchText + ".")
    url = "http://www.google.com/?#q=" + searchText
    webbrowser.open(url=url, new=1, autoraise=True)
'''

COMMANDS_WAKEWORD = ["jarvis"]
COMMANDS_ELIZA = ["let me talk to eliza", "let me talk to elijah"]


class EntityStates(object):
    SLEEPING = 0   # In the sleeping state the entity will wait for one of the wakewords
    LISTENING = 1  # Entity is listening for instructions (not waiting for the wakeword)
    BUSY = 2       # Entity is busy and not ready for instructions

    ALL_STATES = [SLEEPING, LISTENING, BUSY]

    @staticmethod
    def __contains__(state):
        return state in EntityStates.ALL_STATES

class Entity(object):

    STAY_AWAKE_TIME_OUT = 5     # Time in seconds for entity to stay awake without receiving commands

    _thread_exception = None

    @property
    def thread_exception(self):
        """
        This property should be none. If something goes wrong with the entity thread an exception will be kept here
        which can be retrieved by the main thread.
        :return: None or exception
        """
        return self._thread_exception

    @thread_exception.setter
    def thread_exception(self, e):
        """
        Setter
        :param e: Exception to be stored
        :return: None
        """
        self._thread_exception = e
        self.running = False

    _state = EntityStates.SLEEPING
    _previous_state = EntityStates.SLEEPING

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if state not in EntityStates():
            raise AttributeError("Illegal state: " + state)
        if state == EntityStates.SLEEPING:
            print("Going to sleep, activate me using a wakeword.")
            tts.beep()
        self._previous_state = self._state
        self._state = state
        print("Entity entered state " + str(state))

    @property
    def previous_state(self):
        return self._previous_state

    _running = True

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, running):
        self._running = running

    @property
    def voice_recognizer(self):
        return self._voice_recognizer

    @property
    def action_library(self):
        return self._action_library

    def __init__(self):
        self._voice_recognizer = VoiceRecognizer()
        self._action_library = ActionLibrary(self)
        self.interaction_time = time()
        self.eliza = et.Eliza()
        self.elizaMode = False

    def log(self, message):
        print(message)

    def reload_action_library(self):
        self._action_library = ActionLibrary(self)

    def run(self):
        """
        Wrapper around run_voice that adds exception handling. If there is an exception it is stored in the
        thread_exception property and then raised again. This allows the main thread to keep an eye on the entity
        thread.
        :return: None
        """
        try:
            self.run_voice()
        except BaseException as e:
            self.thread_exception = e
            raise e

    def run_voice(self):
        """
        Runs a voice interface allowing interaction with the entity.
        :return: None
        """
        #greeting = self.basic_actions.greet()
        tts.speak("Start up complete.")
        tts.beep()

        while self.running:
            # Busy state
            # After being busy always go to previous state
            if self.state == EntityStates.BUSY:
                self.state = self.previous_state
                # Avoid a Busy state deadlock
                if self.state == EntityStates.BUSY:
                    self.state == EntityStates.SLEEPING

            # Sleeping state
            # Wait for wake word, listen for short phrases
            if self.state == EntityStates.SLEEPING:
                result = self.voice_recognizer.listen(timeout=None, phrase_time_limit=1)
                if result != "":
                    for wakeword in COMMANDS_WAKEWORD:
                        if wakeword in result.lower().split():
                            self.state = EntityStates.BUSY
                            tts.speak("yes")
                            self.interaction_time = time()
                            tts.beep()
                            self.state = EntityStates.LISTENING
                    if self.state == EntityStates.SLEEPING:
                        print("Speak the wakeword to get my attention.")

            # Interaction state
            # Listen for longer phrases and try to process them
            if self.state == EntityStates.LISTENING:
                command = self.voice_recognizer.listen(timeout=None, phrase_time_limit=5)
                if command != "":
                    self.state = EntityStates.BUSY
                    self.interaction_time = time()
                    answer = self.process(command)
                    if answer != "":
                        tts.speak(answer)
                        self.interaction_time = time()
                        self.state = EntityStates.LISTENING
                    # TODO: Implement interrupt command, recognizer has a background listener that could running during responses. Challenge would be to filter out the noise caused by the running response...

                if time() - self.interaction_time > self.STAY_AWAKE_TIME_OUT:
                    self.state = EntityStates.SLEEPING

    def run_cli(self):
        """
        Runs a command line interface allowing to interact with the entity.
        :return: None
        """
        # greeting = self.basic_actions.greet()
        print("Start up complete.")
        tts.beep()

        command = ""
        while self.running:
            command = input(">")
            print(self.process(command))

    def shutdown(self):
        """
        utility instruction to allow actions to shutdown the entity.
        :return: None
        """
        self.running = False

    def sleep(self):
        self.state = EntityStates.SLEEPING

    def process(self, text):
        """
        Process the provided text instruction. The entity will react with a response and potentially additional actions.
        :param text: Instruction to which the entity should react.
        :return: Textual reaction from the entity.
        """

        # Clean up input
        while text[-1] in "!.?": text = text[:-1]
        text = text.lower()

        if text == "":
            return ""

        if self.elizaMode:
            result = self.eliza.respond(text)
            return result

        result = ""

        if result == "":
            result = self.action_library.process(text)

        # Next consider talking to Eliza
        if result == "":
            if text in COMMANDS_ELIZA:
                self.elizaMode = True
                result = "Hello.  How are you feeling today?"
                #TODO: implement exit for Eliza :) should probably convert Eliza mode into an entity state   else: result = "Closing therapy session."

        # # Next try to do something based on the verb
        # tb = TextBlob(text)
        # if result == "":
        #     result = VerbAction.process(tb)

        '''
        if not done:
            if tb.words[0] in COMMANDS_SEARCH:
                searchText = text.split(' ', 1)[1]
                print "AI: Searching the web for " + searchText
                WebSearch(searchText)
        '''

        # question - word definition look up through textblob wordnet
        # What is an elephant?
        # What are elephants?
        # print(tb.tags)
        # VOICE:tell me something about elephants
        # [(u'tell', u'VB'), (u'me', u'PRP'), (u'something', u'NN'), (u'about', u'IN'), (u'elephants', u'NNS')]

        # computer to ask do you like or not? then doe sentiment analysis to get a positive or negative reaction back from human

        if result == "":
            print("NO ACTION!")
            #TODO: Log the question to a logfile for unhandled requests for later review.
        return result
