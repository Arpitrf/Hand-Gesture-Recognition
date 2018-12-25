import socket
from predictor import FrameCapture

def int_to_bytes(value, length):
    result = []
    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    result.reverse()
    return result

def fun():
    x = [19]
    return x

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50009              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
while 1:
    data = conn.recv(1024)
    print("hello", data)
    if data:
        x = FrameCapture("./Sample_images/") 
    if not data: break
    conn.sendall(bytes(x))
conn.close()
