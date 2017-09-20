from actions import Action

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/tasks-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/tasks.readonly'
CLIENT_SECRET_FILE = 'GoogleClientSecret.json'
APPLICATION_NAME = 'Google Tasks API Python Quickstart'

COMMANDS_TASKS = ["what are my to do's", "what are my tasks", "list my tasks", "to do list", "tasks"]

class GoogleActions(Action):

    def __init__(self, entity):
        super(GoogleActions, self).__init__(entity)

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'tasks-python-quickstart.json')

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

    def list_tasks(self):
        """
        Provides a summary of current tasks.
        Tasklist ID is currently hardcoded.

        API documentation: https://developers.google.com/resources/api-libraries/documentation/tasks/v1/python/latest/index.html
        """
        TASKLIST_ID = "MTM5NzE3NjQyMTYwMjY5Nzk0MjQ6MDow"
        credentials = self.get_credentials()
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

    def match(self, command):
        if command in COMMANDS_TASKS:
            return True
        else:
            return False

    def respond(self, command):
        if command in COMMANDS_TASKS:
            return self.list_tasks()
        else:
            return ""

if __name__ == '__main__':
    GA = GoogleActions()
    print(GA.list_tasks())