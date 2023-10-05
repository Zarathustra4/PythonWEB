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

echo_message = client_socket.recv(1024)

print(f"[Echo message] - {echo_message.decode()}")

client_socket.close()