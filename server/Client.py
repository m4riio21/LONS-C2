import socket

class Client:
    """A class representing a client that connects to the server via sockets.

    Attributes:
        host (str): The IP address of the client.
        port (int): The port number used by the client in the socket.
        connection (socket): The connection object created in the server with socket.accept().
    """

    def __init__(self, connection, address):
        """Initializes a new instance of the Client class.

        Args:
            connection (socket): The connection object created in the server with socket.accept().
            address (tuple): The address of the client as a tuple (host, port).
        """
        self.connection = connection
        self.host = address[0]
        self.port = address[1]

    def __str__(self):
        """Returns a string representation of the client in the format host:port"""
        return f"{self.host}:{self.port}"

    def getClientInfo(self):
        """Returns the attributes of the client in a list.

        Returns:
            list: A list containing the connection object, host IP and port number.
        """
        return [self.connection, self.host, self.port]
