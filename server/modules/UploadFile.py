from Server import Server
import base64
import struct

class UploadFile:
    """
    Represents a Submodule that extends the Module class.
    This class handles the modular functionality of uploading a file from the server to the client
    """

    def __init__(self, currentSession, local_file, remote_file):
        """
        Initializes the Submodule with a name and description.
        """

        self.name = "UploadFile"
        self.description = "This module handles the process of uploading a local file to the remote client on a given path."

        self._currentSession = currentSession
        self._local_file = local_file
        self._remote_file = remote_file

    def sendFile(self, server, client, data):
        """
        Sends the file content and filepath on to the remote client
        """

        contents = data[0]
        remote_file_encoded = data[1]

        #Send file contents and where to store it
        server.sendTo(client, b'upload' + remote_file_encoded + b'FILE_START' + contents)



    def openFile(self, path):
        with open(path, 'rb') as f:
            data = f.read()

        return data

    def execute(self):
        """
        Executes the Submodule.
        """

        print(f"Executing Submodule {self.name} - {self.description}")
        server = Server.getInstance()

        # Read file contents
        data = self.openFile(self._local_file)

        # Send data and path
        self.sendFile(server, self._currentSession - 1, [data, self._remote_file.encode('utf-8')])

        return f"Done! File {self._local_file} uploaded to {self._remote_file}"



