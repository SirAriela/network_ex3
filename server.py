import socket
import time

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
    print(data)

    if data:
        if data.__str__() == "what size?":
            HEADER = int(input())
            conn.send(HEADER.__str__().encode(FORMAT))
        i = 0
        total = ""

        try:
            data = conn.recv(HEADER).decode(FORMAT)
            while data:
                print(data)
                total += data
                conn.send(f"ack{i}".encode(FORMAT))
                print(f"ack{i}")
                i = i + 1
                data = conn.recv(HEADER).decode(FORMAT)
                time.sleep(0.1)

                # time.sleep(2)
        except Exception as e:
            print(e)

        print(total)
        conn.close()
