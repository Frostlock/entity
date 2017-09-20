from actions import Action


class ListActions(Action):

    _action_name = "List actions"
    _action_description = "This action provides an overview of all the actions that are available to the entity."
    _command_words = ["list actions", "what can you do", "what can i ask you", "tell me what you can do"]

    def __init__(self, entity):
        super(ListActions, self).__init__(entity)

    def respond(self, command):
        """
        Respond to provided command
        :return: Response
        """
        self.log("List all actions.")
        response = "I currently have " + str(len(self.entity.action_library.actions)) + " defined actions.\n"
        for action in self.entity.action_library.actions:
            response += action.action_name + ":\n"
            response += action.action_description + "\n"
        return response
