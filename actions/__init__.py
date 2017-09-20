
from os.path import dirname, basename, isfile
import glob


class Action(object):
    """
    Super class for all actions.
    """

    @property
    def entity(self):
        return self._entity

    def __init__(self, entity):
        self._entity = entity

    @property
    def command_words(self):
        """
        Command words that trigger this action.
        :return: List of command words
        """
        return self._command_words

    def respond(self, command):
        """
        Respond to provided command
        :return: Response
        """
        raise NotImplementedError("Subclass must implement abstract method: respond(command)")

    def match(self, command):
        """
        Return whether or not this action matches with the provide command
        :return: True or False
        """
        raise NotImplementedError("Subclass must implement abstract method: match(command)")

    def log(self, msg):
        print(msg)
        return


class ActionLibrary(object):
    """
    Collection of all actions available in the actions package.
    It is loaded dynamically at run time. Specifically all classes in the modules in the actions package that
    subclass the Action class are combined in a single ActionLibrary object that can be used by the entity.
    """

    @property
    def entity(self):
        """
        Pointer to the entity object for which this ActionLibrary is generated.
        :return: Entity object
        """
        return self._entity

    @property
    def actions(self):
        """
        List of Action objects
        :return:
        """
        return self._actions

    def __init__(self, entity):
        """
        Initialize the ActionLibrary by loading all Action subclasses from the actions package.
        :param entity: Entity object for which this ActionLibrary is created.
        """
        self._entity = entity
        print("Loading actions from " + dirname(__file__))

        # Find all modules in the package
        python_files = glob.glob(dirname(__file__) + "/*.py")
        module_names = [basename(f)[:-3] for f in python_files if isfile(f) and not f.endswith('__init__.py')]

        # Search the modules for classes that subclass the Action class
        action_classes = []
        for module_name in module_names:
            # Import the module
            module = __import__(__package__ + "." + module_name, globals(), locals(), ['*'])
            md = module.__dict__
            # Action subclasses in the module
            actions = [
                md[c] for c in md if (
                    # is a class
                    isinstance(md[c], type) and md[c].__module__ == module.__name__ and issubclass(md[c], Action)
                )
            ]
            action_classes.extend(actions)

        self._actions = []
        for a in action_classes:
            self._actions.append(a(self.entity))
        print("Loaded " + str(len(self.actions)) + " actions.")

    def process(self, command):
        """
        Process the given command by checking if one of the actions matches. If so use the action to return a result.
        :param command: lower case input string
        :return: response
        """
        for action in self.actions:
            try:
                if action.match(command):
                    return action.respond(command)
            except BaseException as e:
                # To help in identifying where issues are coming from we list the Action class name.
                print("Exception on action object: " + str(action))
                raise e