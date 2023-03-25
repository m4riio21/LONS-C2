import socket
import threading

class Server:
    """A class representing the Server that will handle the socket connections with the clients.

    Attributes:
        socket (Socket): The active socket in the network to establish connection with the clients.
        sessions (Client[]): Array of the Client data structure, containing all information of a Client.
        host (String): host that will serve the Server in the network. By default, localhost.
        port (int): port that will host the Server in the network. By default, 1337.
    """

    _instance = None  # Singleton instance

    def __init__(self, host="0.0.0.0", port=1337):
        if self._instance is not None:
            raise ValueError("An instance of the Server class already exists.")
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.sessions = []
            self.listening = False
            self.server_thread = None
            self.host = host
            self.port = port
            self._instance = self

    @classmethod
    def getInstance(cls, host="0.0.0.0", port=1337):
        """Returns the Singleton instance of the Server class"""
        if cls._instance is None:
            cls._instance = cls(host, port)
        return cls._instance

    def start(self):
        """Binds the socket into the requested host:port, and handles the client connections"""

        def handle_client_connection():
            while self.listening:
                try:
                    connection, client_endpoint = self.socket.accept()
                except socket.timeout:
                    # check for stop flag periodically while waiting for connections
                    if not self.listening:
                        break
                    continue
                self.sessions.append((connection, client_endpoint))
                print("Client #{} - CONNECTED <{}:{}>\n".format(len(self.sessions),client_endpoint[0],client_endpoint[1]))

        endpoint = (self.host, self.port)
        self.socket.bind(endpoint)
        print("Server listening in {}:{}...".format(self.host, self.port))

        self.socket.listen()
        self.listening = True

        self.server_thread = threading.Thread(target=handle_client_connection)
        self.server_thread.start()

    def stop(self):
        """Stops the server from listening to incoming connections"""
        print("Stopping server...")
        self.listening = False
        self.server_thread.join()
        self.socket.close()
        print("Server stopped.")

    def getClients(self):
        """Returns the array of current clients bound to the Server"""
        return self.sessions
