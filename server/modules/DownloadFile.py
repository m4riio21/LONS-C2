from Server import Server
import time

class DownloadFile:
    """
    Represents a Submodule that extends the Module class.
    This class handles the modular functionality of downloading a file from the client to the server

        Attributes:
        connection (socket): The connection object created in the server with socket.accept() where data will be sent and received.
        remote_file (str): The remote file that will be retrieved.
        local_file (str): The local file where the contents will be stored.

    """

    def __init__(self, connection, remote_file, local_file):
        """
        Initializes the Submodule with a name and description.
        """

        self.name = "DownloadFile"
        self.description = "This module handles the process of downloading a remote file from the client into the server."

        self._connection = connection
        self._remote_file = remote_file
        self._local_file = local_file

    def askFile(self, remote_file):
        """
        Sends the desired file to download to the client.
        """
        self._connection.send(b'download' + remote_file)

    def downloadFile(self, local_file):
        """
        Receives the file contents from the socket and writes it into the local file
        """

        file = open(local_file, 'wb')
        chunk = self._connection.recv(1024)
        while chunk:
            try:
                file.write(chunk)
                chunk = self._connection.recv(1024)
            except:
                file.close()
                return True


    def execute(self):
        """
        Executes the Submodule.
        """

        print(f"Executing Submodule {self.name} - {self.description}")
        server = Server.getInstance()

        # Ask the client to deliver the specified file
        self.askFile(self._remote_file.encode())

        # Gets the file contents and saves it in the local path
        code = self.downloadFile(self._local_file)
        print(code)
        if code:
            return f"Done! File {self._remote_file} has been downloaded and saved to {self._local_file}."
        else:
            return f"You don't have permission to save the file to {self._local_file}"

