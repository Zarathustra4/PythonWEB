import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(1)

print("[Listening...]")

connection, client_address = server_socket.accept()
print(f"[Accepted from {connection}, {client_address}]")

try: 
    message = connection.recv(1024)
except Exception as e:
    print(e)
else:
    print("---[Message is recieved]---")
    print(f"\t[Message] - {message.decode()}")
    print(f"\t[Time] - {datetime.now()}")
    print("---------------------------")

connection.close()
