import socket

ip = "192.168.1.8"
port = 9001
bufferSize = 1024

def setIP(ipAddress):
    ip = ipAddress # THIS DOESN'T PROPERLY SET IP

def sendMessage(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(message)
    data = s.recv(bufferSize)
    s.close()
