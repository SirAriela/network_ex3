import socket

# const variables
HEADER = 128
SERVER = 'localhost'
PORT = 5050
FORMAT = 'utf-8'

while True:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER, PORT))
    server_socket.listen(1)
    print("Server is listening...")
    conn, addr = server_socket.accept()
    data = conn.recv(HEADER).decode(FORMAT)
    print("Got connection from", addr)

    if data:
        print(data)
        HEADER = int(data)
        mess = "ack"
        print(mess)
        conn.send(mess.encode(FORMAT))
