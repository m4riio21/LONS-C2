from Server import Server
import ipaddress
import re
import time

class NetInfo:
    """
    Represents a Submodule that extends the Module class.
    This class gathers network information from the remote client, processes it and shows the most important information.

        Attributes:
        connection (socket): The connection object created in the server with socket.accept() where data will be sent and received.
        client_os (str): A string containing the Operative System of the remote client for logic purposes (Windows/Linux).
    """

    def __init__(self, connection, client_os):
        """
        Initializes the Submodule with a name and description.
        """

        self.name = "NetInfo"
        self.description = "This module gathers network information from the remote client, processes it and shows the most important information."

        self._connection = connection
        self._client_os = client_os

    def getOpenPorts(self):
        """
        Gathers the open ports from the remote client
        """

        #Send file contents and where to store it
        self._connection.send(b'netstat')
        data = b''
        time.sleep(0.5)

        #Get data
        while True:
            try:
                chunk = self._connection.recv(1024)
                if not chunk:
                    break
                data += chunk
            except:
                break

        if self._client_os == "Windows":
            local_endpoints_column = '\n'.join(re.findall(r'\S+\s+(\S+:\d+)', data.decode()))
            ipv4_regex_windows = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?::\d+)?\b'
            ipv4_endpoints = re.findall(ipv4_regex_windows, local_endpoints_column)
        else:
            ipv4_regex_linux = r'^\S+\s+\S+\s+\S+\s+(?P<endpoint>\d+\.\d+\.\d+\.\d+:\d+)\s+\S+.*$'
            ipv4_endpoints = re.findall(ipv4_regex_linux, data.decode(), flags=re.MULTILINE)

        return ipv4_endpoints

    def getInterfaces(self):
        """
        Gathers the network interfaces from the remote client
        """

        self._connection.send(b'interfaces')
        data = b''
        time.sleep(0.5)

        # Get data
        while True:
            try:
                chunk = self._connection.recv(1024)
                if not chunk:
                    break
                data += chunk
            except:
                break


        if self._client_os == "Windows":
            def remove_lines_after_netmask(input_string):
                lines = input_string.split("\n")
                output_lines = []
                skip_next_line = False
                for i, line in enumerate(lines):
                    if skip_next_line:
                        skip_next_line = False
                        continue
                    if "255." in line:
                        output_lines.append(line)
                        skip_next_line = True
                    else:
                        output_lines.append(line)
                    if i == len(lines) - 1:  # check if last line has been reached
                        break
                return "\n".join(output_lines)

            input_str = data.decode()

            clean_str = remove_lines_after_netmask(input_str)

            ipv4_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
            matches = re.findall(ipv4_pattern, clean_str)

            nets = []

            for i in range(0, len(matches), 2):
                ip = matches[i]
                netmask = matches[i + 1]

                ip_address = ipaddress.IPv4Address(ip)
                network_address = ipaddress.IPv4Network((ip, netmask), strict=False)
                cidr_net_range = str(network_address)
                nets.append((ip, cidr_net_range))

            return nets

        else:
            input_str = data.decode()
            pattern = re.compile(
                r'inet\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+netmask\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
                re.DOTALL)
            matches = pattern.findall(input_str)
            nets = []
            for match in matches:
                ip_address = ipaddress.IPv4Address(match[0])
                network_address = ipaddress.IPv4Network((match[0], match[1]), strict=False)
                cidr_net_range = str(network_address)
                nets.append((match[0], cidr_net_range))

            return nets

    def makeResults(self, data):
        """
        Returns a filtered string with the ports and networks from the user
        """

        ports = data[0]
        ifaces = data[1]

        all_ifaces = []
        normal_ifaces = []
        for port in ports:
            if port.startswith('0.0.0.0'):
                all_ifaces.append('\t\t' + port)
            else:
                normal_ifaces.append('\t\t' + port)
        stdout = "Ports open on all interfaces:\n"
        stdout += '\n'.join(all_ifaces) + '\n\n'
        stdout += "Ports open on a single interface:\n"
        stdout += '\n'.join(normal_ifaces)
        stdout += '\n\n'

        for n in ifaces:
            ip = n[0]
            net_range = n[1]

            stdout += f"Interface in network range {net_range} with IP address {ip}\n"

        return stdout

    def execute(self):
        """
        Executes the Submodule.
        """

        print(f"Executing Submodule {self.name} - {self.description}")
        server = Server.getInstance()

        #Gather needed information
        ports = self.getOpenPorts()
        ifaces = self.getInterfaces()

        #Make the printable string
        stdout = self.makeResults([ports, ifaces])

        return stdout

