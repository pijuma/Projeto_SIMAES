import socket
import threading

HEADER = 64 # fixed initial header for our protocol that tells the amount of byte (size) of the message the client is going to receive

PORT = 12345

FORMAT = 'utf-8' # format for encoding

DISCONNECT_MESSAGE = '!DISCONNECT' # fixed disconnect message
# SERVER = socket.gethostbyname(socket.gethostname()) # or you can write the ip directly
SERVER = "192.168.0.7"

ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg : str):
    message = msg.encode(FORMAT)

    msg_length = len(message)
    # encodes the message length to bytes
    send_length = str(msg_length).encode(FORMAT)
    print(f"encoded message length: {send_length}")
    
    #  b'' -> binary representation 
    send_length += b' ' * (HEADER - len(send_length)) # adds 64 - n_char (in bytes) of space to complete the 64 fixed header size

    # client.send(send_length)
    client.send(message)


send("78")

# send(DISCONNECT_MESSAGE)