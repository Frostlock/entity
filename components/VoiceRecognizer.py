"""
Voice recognition
"""
import speech_recognition

class VoiceRecognizer(object):

    @property
    def recognizer(self):
        return self._recognizer

    @property
    def latest_recognition(self):
        return self._latest_recognition

    def __init__(self):
        self._recognizer = speech_recognition.Recognizer()
        self._latest_recognition = ""

    def listen(self, timeout=None, phrase_time_limit=None):
        """
        :param timeout: maximum number of seconds that this function will wait for a phrase to start before giving up.
        :param phrase_time_limit: maximum number of seconds that this function will allow a phrase to continue before
            stopping and returning the partial phrase.
        :return: string
        """
        recognitions = None
        print("VoiceRecognizer.py: start listening")
        #to list available Microphones:
        #print speech_recognition.Microphone.list_microphone_names()
        try:
            with speech_recognition.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout, phrase_time_limit)
                print("VoiceRecognizer.py: stop listening")
            # or: return recognizer.recognize_sphinx(audio)
            print("VoiceRecognizer.py: send audio to google")
            recognitions = self.recognizer.recognize_google(audio, show_all=False)
            print("VoiceRecognizer.py: result received: " + str(recognitions))
        except speech_recognition.WaitTimeoutError:
            recognitions = None
        except speech_recognition.UnknownValueError:
            print("VoiceRecognizer.py: Could not understand audio")
        except speech_recognition.RequestError as e:
            print("VoiceRecognizer.py: Recognition Error; {0}".format(e))

        # TODO: google offers alternative interpretations, this can help deal with misunderstandings.
        # You get the alternatives by setting show_all to True
        # The output becomes a dictionary in the following format
        # {u'alternative': [{u'confidence': 0.54517615, u'transcript': u'Jarvis'},
        #                   {u'confidence': 0, u'transcript': u'Travis'},
        #                   {u'confidence': 0, u'transcript': u'service'},
        #                   {u'confidence': 0, u'transcript': u'traverse'},
        #                   {u'confidence': 0, u'transcript': u'carvers'}], u'final': True}

        if recognitions is not None:
            self._latest_recognition = recognitions
        else:
            self._latest_recognition = ""

        return self.latest_recognition

if __name__ == "__main__":
    vr = VoiceRecognizer()
    vr.listen()