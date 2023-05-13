from CommandLineInterface import CommandLineInterface
from Server import Server
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='Hosting of the C&C server.')
    parser.add_argument('port_number', nargs='?', type=int, help='Port number')

    args = parser.parse_args()

    port = args.port_number
    if port == None:
        port = 1337

    cli = CommandLineInterface(port).start()

if __name__ == "__main__":
    main()
    sys.exit(1)