from Server import Server
import ipaddress

class NetInfo:
    """
    Represents a Submodule that extends the Module class.
    This class gathers network information from the remote client, processes it and shows the most important information.
    """

    def __init__(self, currentSession):
        """
        Initializes the Submodule with a name and description.
        """

        self.name = "NetInfo"
        self.description = "This module gathers network information from the remote client, processes it and shows the most important information."

        self._currentSession = currentSession

    def getOpenPorts(self, server, client):
        """
        Gathers the open ports from the remote client
        """

        #Send file contents and where to store it
        server.sendTo(client, b'netstat')
        data = server.recvFrom(client)

        local_endpoints_column = '\n'.join(re.findall(r'\S+\s+(\S+:\d+)', data.decode()))

        ipv4_regex = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?::\d+)?\b'
        ipv4_endpoints = re.findall(ipv4_regex, local_endpoints_column)

        return ipv4_endpoints

    def getInterfaces(self, server, client):
        """
        Gathers the network interfaces from the remote client
        """

        server.sendTo(client, b'interfaces')
        data = server.recvFrom(client)

        if client.getClientOs() == "Windows":
            nets = []
            input_str = """Configuración IP de Windows


                Adaptador de Ethernet VirtualBox Host-Only Network:

                   Sufijo DNS específico para la conexión. . :
                   Vínculo: dirección IPv6 local. . . : fe80::3264:7222:34e0:9582%10
                   Dirección IPv4. . . . . . . . . . . . . . : 192.168.56.1
                   Máscara de subred . . . . . . . . . . . . : 255.255.255.0
                   Puerta de enlace predeterminada . . . . . : 192.168.56.0

                Adaptador de LAN inalámbrica Conexión de área local* 9:

                   Estado de los medios. . . . . . . . . . . : medios desconectados
                   Sufijo DNS específico para la conexión. . :

                Adaptador de LAN inalámbrica Conexión de área local* 10:

                   Estado de los medios. . . . . . . . . . . : medios desconectados
                   Sufijo DNS específico para la conexión. . :

                Adaptador de Ethernet VMware Network Adapter VMnet1:

                   Sufijo DNS específico para la conexión. . :
                   Vínculo: dirección IPv6 local. . . : fe80::412d:5a08:1859:17e8%4
                   Dirección IPv4. . . . . . . . . . . . . . : 192.168.37.1
                   Máscara de subred . . . . . . . . . . . . : 255.255.255.0
                   Puerta de enlace predeterminada . . . . . : 192.168.37.0 

                Adaptador de Ethernet VMware Network Adapter VMnet8:

                   Sufijo DNS específico para la conexión. . :
                   Vínculo: dirección IPv6 local. . . : fe80::e147:f858:9c30:312e%11
                   Dirección IPv4. . . . . . . . . . . . . . : 192.168.79.1
                   Máscara de subred . . . . . . . . . . . . : 255.255.255.0
                   Puerta de enlace predeterminada . . . . . :

                Adaptador de LAN inalámbrica Wi-Fi:

                   Sufijo DNS específico para la conexión. . : technicolor.net
                   Vínculo: dirección IPv6 local. . . : fe80::6d96:5497:f6df:6682%2
                   Dirección IPv4. . . . . . . . . . . . . . : 192.168.0.7
                   Máscara de subred . . . . . . . . . . . . : 255.255.255.0
                   Puerta de enlace predeterminada . . . . . : 192.168.0.1"""
            ipv4_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
            matches = re.findall(ipv4_pattern, input_str)
            print(matches)
            skip_next = False
            j = 0
            n_skips = 0
            print(len(matches))
            if len(matches) >= 2:
                for i in range(0, len(matches), 2):
                    if skip_next == True:
                        j = i + n_skips + 1
                    else:
                        j = i + n_skips
                    if j >= len(matches):
                        break
                    ip = matches[j]
                    netmask = matches[j + 1]

                    print(ip, netmask, skip_next)

                    ip_address = ipaddress.IPv4Address(ip)
                    network_address = ipaddress.IPv4Network((ip, netmask), strict=False)
                    cidr_net_range = str(network_address)
                    nets.append((ip, cidr_net_range))
                    next_ip = ipaddress.IPv4Address(matches[j + 2])
                    if skip_next == True:
                        skip_next = False
                        n_skips = n_skips + 1
                    if next_ip in network_address:
                        skip_next = True

            return nets

        else:
            input_str = """br-95a66a1ac341: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
                        inet 172.18.0.1  netmask 255.255.0.0  broadcast 172.18.255.255
                        inet6 fe80::42:fdff:fe33:1d45  prefixlen 64  scopeid 0x20<link>
                        ether 02:42:fd:33:1d:45  txqueuelen 0  (Ethernet)
                        RX packets 0  bytes 0 (0.0 B)
                        RX errors 0  dropped 0  overruns 0  frame 0
                        TX packets 18  bytes 3792 (3.7 KiB)
                        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

                docker0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
                        inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
                        ether 02:42:cc:18:f6:c3  txqueuelen 0  (Ethernet)
                        RX packets 0  bytes 0 (0.0 B)
                        RX errors 0  dropped 0  overruns 0  frame 0
                        TX packets 0  bytes 0 (0.0 B)
                        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

                eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
                        inet 10.0.2.15  netmask 255.255.255.0  broadcast 10.0.2.255
                        inet6 fe80::a00:27ff:feb1:53e2  prefixlen 64  scopeid 0x20<link>
                        ether 08:00:27:b1:53:e2  txqueuelen 1000  (Ethernet)
                        RX packets 210080  bytes 80347026 (76.6 MiB)
                        RX errors 0  dropped 0  overruns 0  frame 0
                        TX packets 179964  bytes 35364364 (33.7 MiB)
                        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

                lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
                        inet 127.0.0.1  netmask 255.0.0.0
                        inet6 ::1  prefixlen 128  scopeid 0x10<host>
                        loop  txqueuelen 1000  (Local Loopback)
                        RX packets 298  bytes 71551 (69.8 KiB)
                        RX errors 0  dropped 0  overruns 0  frame 0
                        TX packets 298  bytes 71551 (69.8 KiB)
                        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

                tun0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1500
                        inet 10.10.14.56  netmask 255.255.254.0  destination 10.10.14.56
                        inet6 dead:beef:2::1036  prefixlen 64  scopeid 0x0<global>
                        inet6 fe80::d546:740b:7d37:a5f7  prefixlen 64  scopeid 0x20<link>
                        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 500  (UNSPEC)
                        RX packets 173875  bytes 26446492 (25.2 MiB)
                        RX errors 0  dropped 0  overruns 0  frame 0
                        TX packets 163403  bytes 13818570 (13.1 MiB)
                        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

                veth61fa928: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
                        inet6 fe80::3448:43ff:fe89:faf3  prefixlen 64  scopeid 0x20<link>
                        ether 36:48:43:89:fa:f3  txqueuelen 0  (Ethernet)
                        RX packets 0  bytes 0 (0.0 B)
                        RX errors 0  dropped 0  overruns 0  frame 0
                        TX packets 39  bytes 6636 (6.4 KiB)
                        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

                """
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

        for n in nets:
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
        ports = getOpenPorts(server, self._currentSession - 1)
        ifaces = getInterfaces(server, self._currentSession - 1)

        #Make the printable string
        stdout = makeResults([ports, ifaces])

        return stdout

