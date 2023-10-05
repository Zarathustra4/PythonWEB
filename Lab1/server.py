import socket
from datetime import datetime
import time

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
    if not message:
        raise Exception("[Recieve error] - message is empty!")
except Exception as e:
    print(e)
else:
    print("---[Message is recieved]---")
    print(f"[Message] - {message.decode()}")
    print(f"[Time] - {datetime.now()}")
    print("---------------------------")

    print("[Wait for 5 seconds...]")
    time.sleep(5)
    print("[Sending the message back]")
    if len(message) != connection.send(message):
        print("[Not the whole message was sent!!!]")
    else:
        print("[The message was sent successfuly!!!]") 
    

connection.close()
