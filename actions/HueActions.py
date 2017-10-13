from actions import Action

from components import HueInterface

HUE = HueInterface.HueInterface()

class HueActionTurnOn(Action):
    """
    Action to enable Entity to turn on Hue lights.
    """

    _action_name = "Turn on Hue lights"
    _action_description = "Turn on a specific Hue light."
    _command_words = ["lights on", "turn the light on", "turn on the light", "turn on the lights"]

    def __init__(self, entity):
        super(HueActionTurnOn, self).__init__(entity)

    def respond(self, command):
        HUE.turn_on(1)
        return "Turning on the light"

class HueActionTurnOff(Action):
    """
    Action to enable Entity to turn off Hue lights.
    """

    _action_name = "Turn off Hue lights"
    _action_description = "Turn off a specific Hue light."
    _command_words = ["lights out", "lights off", "turn the light off", "turn of the light", "turn of the lights"]

    def __init__(self, entity):
        super(HueActionTurnOff, self).__init__(entity)

    def respond(self, command):
        HUE.turn_off(1)
        return "Turning off the light"