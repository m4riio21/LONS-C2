from Server import Server

class UploadFile:
    """
    Represents a Submodule that extends the Module class.
    This class handles the modular functionality of uploading a file from the server to the client

        Attributes:
        connection (socket): The connection object created in the server with socket.accept() where data will be sent and received.
        local_file (str): The local file that will be uploaded to the client.
        remote_file (str): The remote file location where the file contents will be saved.

    """

    def __init__(self, connection, local_file, remote_file):
        """
        Initializes the Submodule with a name and description.
        """

        self.name = "UploadFile"
        self.description = "This module handles the process of uploading a local file to the remote client on a given path."

        self._connection = connection
        self._local_file = local_file
        self._remote_file = remote_file

    def sendFile(self, data):
        """
        Sends the file content and filepath on to the remote client
        """

        contents = data[0]
        remote_file_encoded = data[1]

        #Send file contents and where to store it
        self._connection.send(b'upload' + remote_file_encoded + b'FILE_START' + contents)

    def openFile(self, path):
        try:
            with open(path, 'rb') as f:
                data = f.read()

            return data
        except:
            return False

    def execute(self):
        """
        Executes the Submodule.
        """

        print(f"Executing Submodule {self.name} - {self.description}")

        # Read file contents
        data = self.openFile(self._local_file)

        # Send data and path
        if data != False:
            self.sendFile([data, self._remote_file.encode('utf-8')])

            code = self._connection.recv(10)

            if b"error" in code:
                return "File couldn't be saved in the client. Specify a valid path."
            else:
                return f"Done! File {self._local_file} uploaded to {self._remote_file}"
        else:
            return f"Invalid file! File doesn't exist or insufficient permissions!"



