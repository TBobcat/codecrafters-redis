import socket

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    conn, addr = server_socket.accept() 

    while True:        
        data = conn.recv(4096)
        print("new connection accepted ! ")
        conn.send(b"+PONG\r\n")

if __name__ == "__main__":
    main()
