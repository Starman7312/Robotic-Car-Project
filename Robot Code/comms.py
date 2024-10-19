import socket
import time
global s

def LAN(host, port, message):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # This initiates the socket object
    connection.settimeout(0.1)
    try:
        connection.connect((host, port)) # This initiates the TCP/IP connection to the server (rec function on rasperry pi)
        connection.sendall(message.encode()) ## This sends the message
        connection.close() ## This closes the connection
    except TimeoutError:
        connection.close()
