from Client import Client
import argparse

def main():
    parser = argparse.ArgumentParser(description='Client-side connection to the C&C server.')
    parser.add_argument('ip_address', nargs='?', type=str, help='IP address')
    parser.add_argument('port_number', nargs='?', type=int, help='Port number')

    args = parser.parse_args()

    if not args.ip_address:
        print('Please provide an IP address')
        return
    if not args.port_number:
        print('Please provide a port number')
        return

    c = Client(args.ip_address, args.port_number)

    c.start()

if __name__ == "__main__":
    main()