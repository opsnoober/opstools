from socket import *


c_sock = socket(AF_INET,SOCK_STREAM)
c_sock.connect(('127.0.0.1',8888))

c_sock.send('cpu'.encode('utf-8'))
data = c_sock.recv(1024).decode('utf-8')
print(data)
c_sock.close()
