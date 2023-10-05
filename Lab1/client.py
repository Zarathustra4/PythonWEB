import socket

HOST = "127.0.0.1"
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

message = input("Input your message >>> ")

try:
    client_socket.send(message.encode())
except Exception as e:
    print(e)
else:
    print("The message was sent")

client_socket.close()