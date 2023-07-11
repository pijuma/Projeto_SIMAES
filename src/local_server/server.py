import socket
import threading

HEADER = 64 # fixed initial header for our protocol that tells the amount of byte (size) of the message the client is going to receive

PORT = 8080
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "192.168.0.15"

ADDR = (SERVER, PORT) # information must be tuple

FORMAT = 'utf-8' # format for encoding

DISCONNECT_MESSAGE = '!DISCONNECT' # fixed disconnect message


#
# WEB_SERVER = "192.168.0.7"
# WEB_PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# web_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# web_server.connect((WEB_SERVER, WEB_PORT))

# def send_msg(msg):
#     msg = msg.encode(FORMAT)

#     web_server.send(msg)

def handle_client(conn : socket, addr : str):
    print(f"New conection from {addr}")

    connected =True
    while connected:
        # blocking line of code
        # receives the header that tells the size of the incomming message
        # msg_length = conn.recv(HEADER).decode(FORMAT)
        # if msg_length: # only convert valid messages
        #     msg_length = int (msg_length)

        # actual message
        msg = conn.recv(256).decode(FORMAT)

        if msg == DISCONNECT_MESSAGE:
            connected = False

        print(f"[{addr}]: {msg}")
        # try:
        #     send_msg(msg)
        # except Exception as err:
        #     print(err)

        
    
    conn.close()

def start():
    server.listen()

    print(f"Listening on {SERVER}")

    while True:
        # blocking line of code
        conn, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        # the amount of threads running represent the amount of clients (+1 for the main thread)
        print(f"Active connections: {threading.activeCount() -1}") 

start()
