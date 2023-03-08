import socket
import selectors
import time
import sys

sel = selectors.DefaultSelector()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 6666))
sel.register(sys.stdin, selectors.EVENT_READ)
sel.register(s, selectors.EVENT_READ)
try:
    while True:
        for key, event in sel.select():
            if key.fileobj is sys.stdin:
                s.sendall(sys.stdin.readline().encode())
            else:
                data = s.recv(1024)
                if data:
                    print(data.decode())
                else:
                    s.close()
                    exit()
except KeyboardInterrupt:
    s.close()
    exit()
