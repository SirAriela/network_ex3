import socket
import time

# const variables
SERVER = 'localhost'
PORT = 5050
FORMAT = 'utf-8'
HEADER = 128


def input_format():
    return {
        "message": "this is test message",
        "max_message_size": 20,
        "window_size": 4,
        "timeout": 5
    }


def text_handle():
    pass


def file_handle():
    pass


try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER, PORT))

    print("Connected to server")

    # print("please select way for client to send message")
    # print("for input text type: text")
    # print("for file input type: file")
    # input_type = input()
    #
    # match input_type:
    #     case "text":
    #         text_handle()
    #     case "file":
    #         file_handle()
    #     case _:
    #         print("input " + input_type + "is not supported")
    max_message_size = input()
    HEADER = int(max_message_size)
    client_socket.send(max_message_size.encode(FORMAT))

    msg = client_socket.recv(1024).decode(FORMAT)
    print(msg)
    client_socket.close()

except:
    print("Failed to connect")
