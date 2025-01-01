import socket
import time
import json

# const variables
HEADER = 128
SERVER = 'localhost'
PORT = 5050
FORMAT = 'utf-8'
file_path = "C:\\Users\\ariel\\PycharmProjects\\ex_3\\tomer.txt"


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

    if len(data) <= HEADER:
        if data.__str__() == "1":
            HEADER = int(input())
            conn.send(HEADER.__str__().encode(FORMAT))
        elif data.__str__() == "2":
            with open(file_path, 'r', encoding=FORMAT) as file:
                data = json.load(file)
                HEADER = data["max_message_size"]
                conn.send(HEADER.__str__().encode(FORMAT))

        total = ""
        i = 0

        try:
            data = conn.recv(HEADER).decode(FORMAT)
            while data:
                seq, msg = data.split("|", 1)
                conn.send(f"ack{seq}".encode(FORMAT))
                print(f"ack{seq}")
                print(msg)

                if i == int(seq):
                    total += msg
                    i += 1
                data = conn.recv(HEADER).decode(FORMAT)
                time.sleep(0.1)

        except Exception as e:
            print(e)

        print(total)
        conn.close()
