import socket
import time
import json

# const variables
SERVER = 'localhost'
PORT = 5050
FORMAT = 'utf-8'
HEADER = 128
file_path = "C:\\Users\\ariel\\PycharmProjects\\ex_3\\tomer.txt"



def text_handle():
    """
    Handles manual text input from the user.
    """
    print("Please enter the message you want to send:")
    return input()


def file_handle():
    """
    Reads content from a file specified by the user and returns it as a string.
    """

    try:
        with open(file_path, 'r', encoding=FORMAT) as file:
            data = json.load(file)

            if not data:
                raise ValueError("The file is empty.")
            print(f"File content read successfully:\n{data}")
            print(data["message"])
            print(int(data["window_size"]))
            print(int(data["timeout"]))
            sliding_window_handle(client_socket,data["message"],data["window_size"],data["timeout"])
    except FileNotFoundError:
        print("Error: File not found. Please check the file path.")
        return None
    except ValueError as ve:
        print(f"Error: {ve}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None



def sliding_window_handle(client_socket_window, message_to_send, window_size, timeout):
    """
    Handles sending the message using a sliding window protocol.
    """
    window_start = 0
    ack_number = -1
    i = 0

    # encode the message we want to send
    message_to_send = message_to_send.encode(FORMAT)

    # create chunks dynamically
    chunks = []
    seq_num = 0

    # for every seq number build max message
    while i < len(message_to_send):
        # calculate the prefix seq number
        prefix_number = len(f"{seq_num}|".encode(FORMAT))
        payload_size = HEADER - prefix_number

        if payload_size <= 0:
            raise ValueError("Invalid payload size, can't send message!")

        chunk = message_to_send[i:i + payload_size]
        chunk = f"{seq_num}|".encode(FORMAT) + chunk
        chunks.append({"seq": seq_num, "data": chunk, "sent_time": 0.0, "ack": False})
        seq_num += 1
        i += payload_size
        print(chunks)

    # all the data is divided into chunks and ready to be sent
    window_end = min(window_start + window_size, len(chunks))

    while window_start < len(chunks):
        for i in range(window_start, window_end):
            current_time = time.time()

            if not chunks[i]["ack"] and (
                    chunks[i]["sent_time"] == 0.0 or (current_time - chunks[i]["sent_time"]) > timeout):
                client_socket_window.send(chunks[i]["data"])
                chunks[i]["sent_time"] = current_time
                print("sent: ", chunks[i]["data"])

        try:
            client_socket_window.settimeout(timeout)
            ack_data = client_socket_window.recv(128).decode(FORMAT)

            if "ack" in ack_data:
                current_ack_number = int(ack_data.replace("ack", ""))
                print(current_ack_number)
                print(ack_number + 1)
                if ack_number + 1 == current_ack_number:
                    chunks[current_ack_number]["ack"] = True
                    ack_number += 1
                    window_start += 1
                    window_end = min(window_end + 1, len(chunks))

        except socket.timeout:
            print("Timeout occurred, resending unacknowledged chunks.")

    client_socket_window.close()


if __name__ == '__main__':

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER, PORT))

        if not client_socket:
            client_socket.close()
            raise "Socket connection broken"

        print("Connected to server")

        # User chooses between text input or file input
        print("Select input type:")
        print("1 - Text input")
        print("2 - File input")
        input_type = input()

        # Handle input type
        if input_type == "1":
            message = text_handle()
        elif input_type == "2":
            client_socket.send(input_type.encode(FORMAT))
            HEADER = int(client_socket.recv(HEADER).decode(FORMAT))
            file_handle()

        # Check max size with server
    #    size_request = "what size?"
     #   client_socket.send(size_request.encode(FORMAT))
      #  size_response = client_socket.recv(HEADER).decode(FORMAT)



    except socket.error:
        print("Socket broken")