import socket

HOST = "127.0.0.1"
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

message = ""

while message != "CLOSE": 
    print("\n----------------------------\n")
    message = input("Input your message >>> ")

    client_socket.send(message.encode())
    print("The message was sent")

    echo_message = client_socket.recv(1024)

    print(f"[Echo message] - {echo_message.decode()}")
    print("\n----------------------------\n")

client_socket.close()