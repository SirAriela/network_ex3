import socket
import time

# const variables
SERVER = 'localhost'
PORT = 5050
FORMAT = 'utf-8'

# the size of a single msg
HEADER = 128


def text_handle():
    pass


def file_handle():
    pass


def sliding_window_handle(client_socket_window, message_to_send):
    base = 0
    current_sequence = 0

    message_to_send = message_to_send.encode(FORMAT)
    x = [message_to_send[i:i + HEADER] for i in range(0, len(message_to_send), HEADER)]
    print(x)

    for i in x:
        client_socket_window.send(i)
        print(client_socket_window.recv(1024).decode(FORMAT))



try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER, PORT))
    if not client_socket:
        client_socket.close()
        raise "socket connection broken"

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

    # check from server what is the max size of a single msg
    size_request = "what size?"
    client_socket.send(size_request.encode(FORMAT))

    # the size of a max msg
    size_response = client_socket.recv(HEADER).decode(FORMAT)

    if not size_response:
        raise "invalid header size"

    else:
        HEADER = int(size_response)
        message = input()
        sliding_window_handle(client_socket, message)

        client_socket.close()

except socket.error:
    print("Socket broken")
