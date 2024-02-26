import os
def get_connection_args(filepath: str = None):
    """Returns the connection hostname and port
    filepath: None -> './ReviewAPP/ngrok.txt'
    """

    if filepath is None:
        filename = './ReviewAPP/ngrok.txt'

    with open(filename, 'r') as file:
        hostname = file.readline()
        forward_ip, forward_port = hostname.split('://')[1].split(':')
        forward_port = int(forward_port)

        return forward_ip, forward_port