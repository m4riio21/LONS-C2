from CommandLineInterface import CommandLineInterface
from Server import Server

def main():
    server1 = Server.getInstance()
    server2 = Server.getInstance()
    print(server1 == server2)
    cli = CommandLineInterface().start()

if __name__ == "__main__":
    main()