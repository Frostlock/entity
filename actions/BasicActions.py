from actions import Action
from datetime import datetime
from random import choice

ACTION_GROUP = "Basic actions"
ACTION_GROUP_DESCRIPTION = "A number of direct question and response combinations."


class BasicActionGreet(Action):

    _action_name = "Greet"
    _action_description = "This action enables the entity to respond to greetings."
    _command_words = ["hi", "hello", "good morning", "morning", "good afternoon", "good evening"]

    def __init__(self, entity):
        super(BasicActionGreet, self).__init__(entity)

    def respond(self, command):
        self.log("Respond to greeting.")
        hour = int(datetime.strftime(datetime.now(), "%H"))
        if hour < 12:
            return "Good morning"
        elif hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"


class BasicActionStatusReport(Action):

    _action_name = "Status report"
    _action_description = "This action provides a status report."
    _command_words = ["status", "how are you"]

    def __init__(self, entity):
        super(BasicActionStatusReport, self).__init__(entity)

    def respond(self, command):
        self.log("Report status")
        return "System online and fully operational."


class BasicActionShutdown(Action):
    _action_name = "Shutdown"
    _action_description = "This action shuts down the entity."
    _command_words = ["exit", "quit", "shutdown", "shutdown system", "goodbye", "shut down"]

    def __init__(self, entity):
        super(BasicActionShutdown, self).__init__(entity)

    def respond(self, command):
        self.log("Initiating shutdown")
        self.entity.shutdown()
        return "Goodbye"


class BasicActionSleep(Action):
    _action_name = "Sleep"
    _action_description = "This action puts the entity in sleep mode."
    _command_words = ["sleep", "go to sleep", "nevermind", "talk to yo later"]

    def __init__(self, entity):
        super(BasicActionSleep, self).__init__(entity)

    def respond(self, command):
        self.log("Going to sleep")
        self.entity.sleep()
        return ""


class BasicActionRespondToThanks(Action):
    _action_name = "Respond to thanks"
    _action_description = "This action allowa the entity to respond to a thank you statement."
    _command_words = ["thanks", "thank you", "merci"]

    def __init__(self, entity):
        super(BasicActionRespondToThanks, self).__init__(entity)

    def respond(self, command):
        self.log("Respond to thanks")
        answer = choice(
            ["No problem.", "You're welcome.", "No problem!", "you're welcome.", "sure", "Happy to serve!"])
        return answer


class BasicActionStateTime(Action):
    _action_name = "State time"
    _action_description = "This makes the entity state the current time."
    _command_words = ["what time is it", "what is the time", "time", "time please"]

    def __init__(self, entity):
        super(BasicActionStateTime, self).__init__(entity)

    def respond(self, command):
        self.log("State time")
        return "Its " + datetime.strftime(datetime.now(), "%H:%M") + "."


class BasicActionStateDate(Action):
    _action_name = "State date"
    _action_description = "This makes the entity state the current date."
    _command_words = ["what day is it", "what date is it", "what is the date", "date", "date please"]

    def __init__(self, entity):
        super(BasicActionStateDate, self).__init__(entity)

    def respond(self, command):
        self.log("State date")
        return "Its " + datetime.strftime(datetime.now(), "%A %B %d %Y") + "."


class BasicActionRespondToComplaint(Action):
    _action_name = "Respond to complaint"
    _action_description = "This enables the entity to respond to complaint statements."
    _command_words = ["finally", "that took long enough"]

    def __init__(self, entity):
        super(BasicActionRespondToComplaint, self).__init__(entity)

    def respond(self, command):
        self.log("Respond to complaint")
        answer = choice(["Sorry.", "Apologies.", "I'm doing my best!"])
        return answer