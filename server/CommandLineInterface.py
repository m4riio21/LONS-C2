import colorama
from Server import Server
import os
import sys

class CommandLineInterface:
    """A class representing a command-line interface that handles the user input.

    Attributes:
        currentSession (int): Number of the current session the user is managing.
        commandHistory (String[]): Historic of all the commands ran by the user.
    """

    def __init__(self, currentSession=0, commandHistory=[]):
        self._currentSession = currentSession
        self._commandHistory = commandHistory

    def start(self):
        """Starts the command-line interface logic"""
        self.server = Server.getInstance()
        self.server.start()
        self.commandHandler()

    def getActiveSessions(self):
        """Gets the active sessions managed by the Server."""
        pass

    def selectActiveSession(self, session):
        """Changes the current active session.

        Args:
            session (int): The session id to change to.
        """

        if type(session) == int:# and
            self._currentSession = session

    def commandHandler(self):
        """Creates a pseudo-console, and handles input entered by the user"""

        user = os.getlogin().lower()

        prompt = f"{user}@sazo> "
        print("Type help to see options")

        while True:
            # Print the prompt and read user input

            user_input = input(prompt)

            if user_input == '':
                pass
            if user_input == 'help':
                print("test")
            if user_input == 'exit':
                self.server.stop()
                sys.exit(1)

    def showResults(self):
        """Shows in command-line the corresponding results requested by the user."""
