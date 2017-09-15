import components.ElizaTherapist as et

from actions.BasicActions import BasicActions
from actions.GoogleActions import GoogleActions
#from actions.VerbAction import VerbAction
#from textblob import TextBlob

import components.TextToSpeech as tts
import components.VoiceRecognition as vr

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
    SLEEPING = 0     # In the sleeping state the entity will wait for one of the wakewords
    INTERACTION = 1  # Interaction state is right after waking, in this state the entity does not wait for the wakeword

    ALL_STATES = [SLEEPING,INTERACTION]

    @staticmethod
    def __contains__(state):
        return state in EntityStates.ALL_STATES

class Entity(object):

    STAY_AWAKE_TIME = 5  # Time in seconds for entity to stay awake.

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
        self._state = state

    def __init__(self):
        self.basic_actions = BasicActions(self)
        self.google_actions = GoogleActions()
        self.loop = True
        self.state = EntityStates.SLEEPING
        self.interaction_time = time()

        self.eliza = et.Eliza()
        self.elizaMode = False

    def run(self):
        """
        Runs a voice interface allowing interaction with the entity.
        :return: None
        """
        greeting = self.basic_actions.greet()
        tts.speak(greeting)
        tts.beep()

        while self.loop:

            # Sleeping state
            # Wait for wake word, listen for short phrases
            if self.state == EntityStates.SLEEPING:
                result = vr.listen(timeout=None, phrase_time_limit=1)
                if result != "":
                    for wakeword in COMMANDS_WAKEWORD:
                        if wakeword in result.lower().split():
                            self.state = EntityStates.INTERACTION
                            tts.speak("yes")
                            self.interaction_time = time()
                            tts.beep()
                    if self.state == EntityStates.SLEEPING:
                        print("Speak the wakeword to get my attention.")

            # Interaction state
            # Listen for longer phrases and try to process them
            if self.state == EntityStates.INTERACTION:
                command = vr.listen(timeout=None, phrase_time_limit=5)
                if command != "":
                    self.interaction_time = time()
                    answer = self.process(command)
                    if answer != "":
                        tts.speak(answer)
                        self.interaction_time = time()
                    # TODO: Implement interrupt command, recognizer has a background listener that could running during responses. Challenge would be to filter out the noise caused by the running response...

                if time() - self.interaction_time > self.STAY_AWAKE_TIME:
                    self.state = EntityStates.SLEEPING

    def run_cli(self):
        """
        Runs a command line interface allowing to interact with the entity.
        :return: None
        """
        greeting = self.basic_actions.greet()
        print(greeting)

        command = ""
        while self.loop:
            command = input(">")
            print(self.process(command))

    def shutdown(self):
        """
        utility instruction to allow actions to shutdown the entity.
        :return: None
        """
        self.loop = False

    def sleep(self):
        self.state = EntityStates.SLEEPING

    def process(self, text):
        """
        Process the provided text instruction. The entity will react with a response and potentially additional actions.
        :param text: Instruction to which the entity should react.
        :return: Textual reaction from the entity.
        """

        ''' Clean up input '''
        while text[-1] in "!.": text = text[:-1]
        text = text.lower()

        if text == "":
            return ""

        if self.elizaMode:
            result = self.eliza.respond(text)
            return result

        result = ""

        # First do basic actions
        if result == "":
            result = self.basic_actions.process(text)

        # Next try some google actions
        if result == "":
            result = self.google_actions.process(text)

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
