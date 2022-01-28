import socket

s = socket.socket()
host = "localhost"
port = 12345
s.connect((host, port))

file = open("image.png", "rb")
imgData = file.read()

s.send(imgData)

s.close()