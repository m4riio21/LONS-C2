import socket
import os
import re
import subprocess

class Client:
    """A class representing a client that connects to the server via sockets.

    Attributes:
        host (str): The IP address of the client.
        port (int): The port number used by the client in the socket.
        connection (socket): The connection object created in the server with socket.accept().
    """

    def __init__(self, connection, address, os):
        """Initializes a new instance of the Client class.

        Args:
            connection (socket): The connection object created in the server with socket.accept().
            address (tuple): The address of the client as a tuple (host, port).
            os (String): A string representing the operative system of the client (Windows / Linux).
        """
        self.connection = connection
        self.host = address[0]
        self.port = address[1]
        self.os = os

    def getClientOs(self):
        """
        Gets the OS of the client (Windows / Linux)
        """
        ttl = None
        if os.name == 'nt':
            result = subprocess.run(["ping", "-n", "1", f"{self.host}"], capture_output=True, text=True)
            ttl_match = re.search(r"TTL=(\d+)", result.stdout)
            ttl = ttl_match.group(1)
        elif os.name == 'posix':
            result = subprocess.run(["ping", "-c", "1", f"{self.host}"], capture_output=True, text=True)
            ttl_match = re.search(r"TTL=(\d+)", result.stdout)
            ttl = ttl_match.group(1)

        ttl = int(ttl)

        if ttl == None:
            return None
        else:
            if ttl >= 127:
                return "Windows"
            else:
                if ttl <= 65:
                    return "Linux"
                else:
                    return None

    def __str__(self):
        """Returns a string representation of the client in the format host:port"""
        return f"{self.host}:{self.port}"

    def getClientInfo(self):
        """Returns the attributes of the client in a list.

        Returns:
            list: A list containing the connection object, host IP and port number.
        """
        return [self.connection, self.host, self.port, self.os]
