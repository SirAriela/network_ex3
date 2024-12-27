import socket

# const variables
HEADER = 128
SERVER = 'localhost'
PORT = 5050
FORMAT = 'utf-8'


def input_format():
    return {
        "message": "this is test message",
        "max_message_size": 20,
        "window_size": 4,
        "timeout": 5
    }


while True:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER, PORT))
    server_socket.listen(1)
    print("Server is listening...")
    conn, addr = server_socket.accept()
    print("Got connection from", addr)

    data = conn.recv(HEADER).decode(FORMAT)

    if data:
        if data.__str__() == "what size?":
            HEADER = int(input())
            conn.send(HEADER.__str__().encode(FORMAT))
        i = 0
        total = ""

        mess = "ack"

        data = conn.recv(HEADER).decode(FORMAT)
        while data:
            total += data
            conn.send((mess + i.__str__()).encode(FORMAT))
            i = i + 1
            data = conn.recv(HEADER).decode(FORMAT)

        print(total)
