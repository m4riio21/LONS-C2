from colorama import init, Fore, Back, Style
import socket
import threading
import select
import time
import ssl
from Client import Client

class Server:
    """A class representing the Server that will handle the socket connections with the clients.

    Attributes:
        socket (Socket): The active socket in the network to establish connection with the clients.
        sessions (Client[]): Array of the Client data structure, containing all information of a Client.
        host (String): host that will serve the Server in the network. By default, localhost.
        port (int): port that will host the Server in the network. By default, 1337.
    """

    _instance = None

    def __init__(self, host="0.0.0.0", port=1337):
        if self._instance is not None:
            raise ValueError("An instance of the Server class already exists.")
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.clients = []
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
                    connection.settimeout(1)
                    control_connection, client_endpoint_control = self.control_socket.accept()
                    data = control_connection.recv(3)
                except socket.timeout:
                    # check for stop flag periodically while waiting for connections
                    if not self.listening:
                        break
                    continue
                if data == b'WIN':
                    client_os = 'Windows'
                elif data == b'LIN':
                    client_os = 'Linux'

                new_client = Client(control_connection, connection, client_endpoint, client_os)
                self.clients.append(new_client)

                print("Client #{} - CONNECTED <{}:{}>".format(len(self.clients),client_endpoint[0],client_endpoint[1]))

        def handle_disconnected():
            while self.listening:
                # Sleep for 1 second between clients to avoid overloading the server
                time.sleep(1)

                for client in self.clients:
                    control_connection = client.getClientInfo()[0]
                    control_connection.settimeout(1)
                    try:
                        # Check if each client connection is still active
                        data = control_connection.recv(1024)
                        if not data:
                            self.clients.remove(client)
                            print(f"Connection with client {client} has been closed")
                    except:
                        pass



        endpoint = (self.host, self.port)
        control_endpoint = (self.host, 65000)
        self.socket.bind(endpoint)
        self.control_socket.bind(control_endpoint)
        print("Server listening in {}:{}...".format(self.host, self.port))

        self.socket.listen()
        self.control_socket.listen()
        self.listening = True

        self.server_thread = threading.Thread(target=handle_client_connection)
        self.disconnected_thread = threading.Thread(target=handle_disconnected)
        self.disconnected_thread.start()
        self.server_thread.start()

    def stop(self):
        """Stops the server from listening to incoming connections"""
        print(Fore.RED + "Stopping server..." + Style.RESET_ALL)
        self.listening = False
        self.server_thread.join()
        self.disconnected_thread.join()
        self.socket.close()
        self.control_socket.close()
        print(Fore.RED + "Server successfully stopped!" + Style.RESET_ALL)

    def getClients(self):
        """Returns the array of active clients with the relevant information of each client"""
        ret = []
        for c in self.clients:
            ret.append(c.getClientInfo())

        return ret

    def getClient(self, client_pos):
        """Returns the Client object given a position in the self.clients array"""
        return self.clients[client_pos]

    def getConnection(self, client_pos):
        """Returns a Socket connection object given a position in the self.clients array."""
        return self.clients[client_pos].getClientInfo()[1]


    def deleteClient(self, pos):
        """Deletes a client based on position in self.clients"""
        c = self.clients[pos - 1].getClientInfo()

        #Get connection
        c[0].close()
        c[1].close()

        #Remove client from the array
        del self.clients[pos - 1]


