from actions import Action

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.client import HttpAccessTokenRefreshError
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/tasks-python-quickstart.json
SCOPES = "https://www.googleapis.com/auth/tasks"
CLIENT_SECRET_FILE = "GoogleClientSecret.json"
APPLICATION_NAME = "Google Tasks API Python Quickstart"

CREDENTIAL_DIR = ".credentials"
CREDENTIAL_FILE = "tasks-python-quickstart.json"

ACTION_GROUP = "Google services"
ACTION_GROUP_DESCRIPTION = "Access to several Google services."


def clear_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, CREDENTIAL_DIR)
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, CREDENTIAL_FILE)
    os.remove(credential_path)

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, CREDENTIAL_DIR)
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, CREDENTIAL_FILE)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


class GoogleActionListTasks(Action):
    """
    Action to enable Entity to list current tasks on Google tasklist
    Based on example : https://developers.google.com/google-apps/tasks/quickstart/python
    """

    _action_name = "List Google tasks"
    _action_description = "List current google tasks."
    _command_words = ["what are my to do's", "what are my tasks", "list my tasks", "to do list", "tasks", "list tasks"]

    def __init__(self, entity):
        super(GoogleActionListTasks, self).__init__(entity)

    def respond(self, command):
        """
        Provides a summary of current tasks.
        Tasklist ID is currently hardcoded.

        API documentation: https://developers.google.com/resources/api-libraries/documentation/tasks/v1/python/latest/index.html
        """
        TASKLIST_ID = "MTM5NzE3NjQyMTYwMjY5Nzk0MjQ6MDow"

        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('tasks', 'v1', http=http)
        try:
            results = service.tasks().list(tasklist=TASKLIST_ID).execute()
        except HttpAccessTokenRefreshError as e:
            print(e)
            print("Clearing credentials and tyring again.")
            clear_credentials()
            credentials = get_credentials()
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('tasks', 'v1', http=http)
            results = service.tasks().list(tasklist=TASKLIST_ID).execute()

        items = results.get('items', [])
        if not items:
            return "Your task list is empty."
        else:
            answer = "You have " + str(len(items)) + " tasks: "
            for item in items:
                if item['title'].strip() == "":
                    answer += "a task without title, "
                else:
                    answer += item['title'] + ", "
            return answer[:-2]


class GoogleActionAddTask(Action):
    """
    Enables Entity to add a new task to the Google tasklist
    """

    _action_name = "Add Google task"
    _action_description = "Add a new task to the Google tasklist."
    _command_words = ["add task", "new task", "create task"]

    def __init__(self, entity):
        super(GoogleActionAddTask, self).__init__(entity)

    def match(self, command):
        """
        Return whether or not this action matches with the provide command
        :return: True or False
        """
        for command_start in self.command_words:
            if command.startswith(command_start):
                return True
        return False

    def respond(self, command):
        """
        Adds a task to the tasklist.
        Tasklist ID is currently hardcoded.

        Documentation: https://developers.google.com/google-apps/tasks/v1/reference/tasks/insert
        """
        TASKLIST_ID = "MTM5NzE3NjQyMTYwMjY5Nzk0MjQ6MDow"

        task_title = ""
        for command_start in self.command_words:
            if command.startswith(command_start):
                task_title = command.lstrip(command_start).lstrip()  # Also remove likely space
                break

        if task_title == "":
            return "Please repeat command and add a name for the new task."

        task = {
            'title': task_title,
            'notes': "Task added by entity"
        }

        try:
            credentials = get_credentials()
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('tasks', 'v1', http=http)
            result = service.tasks().insert(tasklist=TASKLIST_ID, body=task).execute()
            return "Task added"
        except HttpAccessTokenRefreshError as e:
            print(e)
            print("Clearing credentials and tyring again.")
            clear_credentials()
            credentials = get_credentials()
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('tasks', 'v1', http=http)
            result = service.tasks().insert(tasklist=TASKLIST_ID, body=task).execute()
            return "Task added"

if __name__ == '__main__':
    GA = GoogleActionListTasks(None)
    print(GA.respond("brol"))
