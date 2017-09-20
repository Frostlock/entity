from actions import Action
from datetime import datetime
from random import choice

"""
Command words for basic actions
These have to be lower case and without punctuation.
"""
COMMANDS_GREET = ["hi", "hello", "good morning", "morning", "good afternoon", "good evening"]
COMMANDS_STATUS = ["status"]
COMMANDS_SHUTDOWN = ["exit", "quit", "shutdown", "shutdown system", "goodbye", "shut down"]
COMMANDS_SLEEP = ["sleep", "go to sleep", "nevermind", "talk to yo later"]
COMMANDS_THANK = ["thanks", "thank you", "merci"]
COMMANDS_TIME = ["what time is it", "what is the time", "time", "time please"]
COMMANDS_DATE = ["what day is it", "what date is it", "what is the date", "date", "date please"]
COMMANDS_FINALLY = ["finally", "that took long enough"]


class BasicActions(Action):

    _action_name = "Basic actions"
    _action_description = "A number of direct question and response combinations."

    def __init__(self, entity):
        super(BasicActions, self).__init__(entity)
        self.ACTIONS = [
            (COMMANDS_GREET, self.greet),
            (COMMANDS_STATUS, self.status),
            (COMMANDS_SHUTDOWN, self.shutdown),
            (COMMANDS_SLEEP, self.sleep),
            (COMMANDS_THANK, self.respond_to_thanks),
            (COMMANDS_TIME, self.state_time),
            (COMMANDS_DATE, self.state_date),
            (COMMANDS_FINALLY, self.respond_to_complaint)
        ]

    def match(self, command):
        for commands, func in self.ACTIONS:
            if command in commands: return True
        return False

    def respond(self, command):
        """
        Process instruction, return answer if found
        :param command: instruction
        :return: string (answer or "")
        """
        for commands, func in self.ACTIONS:
            if command in commands: return func()
        return ""

    def greet(self):
        self.log("Greet")
        hour = int(datetime.strftime(datetime.now(), "%H"))
        if hour < 12:
            return "Good morning"
        elif hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"

    def status(self):
        self.log("Report status")
        return "System online and fully operational"

    def shutdown(self):
        self.log("Initiating shutdown")
        self.entity.shutdown()
        return "Goodbye"

    def sleep(self):
        self.log("Going to sleep")
        self.entity.sleep()
        return ""

    def respond_to_thanks(self):
        self.log("Respond to thanks")
        answer = choice(["No problem.", "You're welcome.", "No problem!", "you're welcome.", "sure", "Happy to serve!"])
        return answer

    def state_time(self):
        self.log("State time")
        return "Its " + datetime.strftime(datetime.now(), "%H:%M") + "."

    def state_date(self):
        self.log("State date")
        return "Its " + datetime.strftime(datetime.now(), "%A %B %d %Y") + "."

    def respond_to_complaint(self):
        self.log("Respond to complaint")
        answer = choice(["Sorry.", "Apologies.", "I'm doing my best!"])
        return answer