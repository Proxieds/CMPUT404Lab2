import socket
# Import Process daemon from multiprocessing to handle multiple requests
from multiprocessing import Process

"""
Defining global variables and setting the buffer size
"""
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
    # Create Socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_server:
        print("Starting Proxy Server...")
        # Reuse addresses, bind and set to listening mode
        proxy_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_server.bind((HOST, PORT))
        proxy_server.listen(2)

        while True:
            # Accept connections and start the process daemon for handling multiple connections
            conn,addr = proxy_server.accept()
            process = Process(target=handle_echo, args=(addr, conn))
            process.daemon = True
            process.start()
            print("Started Process ", process)

def handle_echo(addr, conn):
    """
    Sends connections back to the client
    """
    print("Connected by", addr)

    data = conn.recv(BUFFER_SIZE)
    conn.sendall(data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

if __name__ == "__main__":
    main()