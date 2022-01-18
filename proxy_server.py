import socket, sys

"""
Defining global variables and setting the buffer size
"""
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def get_remote_ip(host):
    """
    Gets the ip address
    """
    print("Getting ip for %s" %host)
    try:
        remote_ip = socket.gethostbyname(host)
    except:
        print("Hostname could not be resolved. Exiting")
        sys.exit()

    print("Ip address of %s is %s" % (host, remote_ip))
    return remote_ip

def main():
    # Part 6
    host = "www.google.com"
    port = 80

    # Create Socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_server:
        print("Starting Proxy Server...")
        # Reuse addresses, bind and set to listening mode
        proxy_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_server.bind((HOST, PORT))
        proxy_server.listen(1)

        while True:
            # Connect proxy_server
            conn, addr = proxy_server.accept()
            print("Connected by", addr)

            # Create a temporary client socket to forward data to a different server socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_client:
                print("Connecting to Google")
                remote_ip = get_remote_ip(host)
                
                # Connect proxy client
                proxy_client.connect((remote_ip, port))

                # Send data to google
                send_full_data = conn.recv(BUFFER_SIZE)
                print("Sending received data %s to google" % send_full_data)
                proxy_client.sendall(send_full_data)

                # Shuts down the client socket
                proxy_client.shutdown(socket.SHUT_WR)

                data = proxy_client.recv(BUFFER_SIZE)
                print("Sending received data: %s to the client" % data)
                # Sends the data back to client
                conn.send(data)

                conn.close

if __name__ == "__main__":
    main()
