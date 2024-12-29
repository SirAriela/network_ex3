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


# def check_timer(timers , timeout):
#     current_time = time.time()
#     for seq, timestamp in timers.items():
#         if current_time - timestamp > timeout:
#             return True


def sliding_window_handle(client_socket_window, message_to_send, window_size, timeout):
    window_start = 0
    ack_number = -1

    # encode the message we want to send
    message_to_send = message_to_send.encode(FORMAT)
    # break it into chunks
    chunks = [message_to_send[i:i + HEADER] for i in range(0, len(message_to_send), HEADER)]
    # see what's bigger the window size or the amount of chunks
    window_end = min(window_size, len(chunks))
    # we make a list for each message we define which seq number, the msg, timer and whether it's ack or not.
    messages = [{"seq": i, "data": chunks[i], "sent_time": 0.0, "acknowledged": False} for i in range(len(chunks))]

    # while there is more messages to send
    while window_start < len(chunks):
        # we send the messages  in the window
        for i in range(window_start, window_end):
            if not messages[i]["acknowledged"] and (messages[i]["sent_time"] - time.time() > timeout or messages[i]["sent_time"] == 0.0):
                client_socket_window.send(messages[i]["data"])
                messages[i]["sent_time"] = time.time()
                print("sent:")
                print(chunks[i])

        try:
            # wait for ack
            current_ack_number = client_socket_window.recv(128).decode(FORMAT)
            print(current_ack_number)
            if "ack" in current_ack_number:
                current_ack_number = int(current_ack_number.replace("ack", ""))

                if ack_number + 1 == current_ack_number:
                    messages[current_ack_number]["acknowledged"] = True
                    ack_number += 1
                    window_start += 1
                    window_end = min(window_end + 1, len(chunks))
        except socket.timeout:
            print("problem")
    # ------------------------------------------------------------------------------------------------------

    # while base < window_size:
    #     while current_sequence < base + window_size:
    #         client_socket_window.send(x[current_sequence].encode(FORMAT))
    #         timers[current_sequence] = time.time()
    #         current_sequence += 1
    #
    #     try:
    #         current_msg = client_socket_window.recv(HEADER).decode(FORMAT)
    #         if current_msg.__contains__("ack"):
    #             current_ack_number = int(current_msg.replace("ack", ""))
    #             if ack_number + 1 == current_ack_number:
    #                 base = base + 1
    #                 ack_number = ack_number + 1
    #                 del timers[ack_number]

    #
    #     except socket.timeout:
    #         raise "Connection timed out"
    #
    # print(x)
    #
    # for i in x:
    #     client_socket_window.send(i)
    #     print(client_socket_window.recv(1024).decode(FORMAT))


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
        print("input the message you want to send")
        message = input()
        print("input the size of sliding widow")
        window_size1 = int(input())
        print("input time")
        timeout1 = int(input())

        sliding_window_handle(client_socket, message, window_size1, timeout1)
        client_socket.close()

except socket.error:
    print("Socket broken")
