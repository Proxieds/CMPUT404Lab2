import socket
# Import Process daemon from multiprocessing to handle multiple requests
from multiprocessing import Process

"""
Defining global variables and setting the buffer size
"""
HOST = "localhost"
PORT = 8001
BUFFER_SIZE = 1024

payload = "GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n"

def connect(addr):
    """
    Creates socket, connects and receives data
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        s.sendall(payload.encode())
        s.shutdown(socket.SHUT_WR)

        full_data = s.recv(BUFFER_SIZE)
        print(full_data)
    
    except Exception as e:
        print(e)

    finally:
        # Close socket 
        s.close()

def main():
    # Start process for handling connection requests to proxy server
    process = Process(target=connect, args=((HOST, PORT),))
    process.start()
    process.join()

if __name__ == "__main__":
    main()
