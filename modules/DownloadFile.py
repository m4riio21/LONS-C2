from Server import Server


class DownloadFile:
    """
    Represents a Submodule that extends the Module class.
    This class handles the modular functionality of downloading a file from the client to the server
    """

    def __init__(self, currentSession, remote_file, local_file):
        """
        Initializes the Submodule with a name and description.
        """

        self.name = "DownloadFile"
        self.description = "This module handles the process of downloading a remote file from the client into the server."

        self._currentSession = currentSession
        self._remote_file = remote_file
        self._local_file = local_file

    def askFile(self, server, client, file):
        """
        Sends the desired file to download to the client.
        """
        server.sendTo(client, b'download' + file)

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
        askFile(server, self._currentSession - 1, self._remote_file.encode())

        # Gets the file contents and saves it in the local path
        downloadFile(server, self._currentSession - 1, self._local_file)

        return f"Done! File {self._remote_file} has been downloaded and saved to {self._local_file}."

