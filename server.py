import socket
import selectors
from datetime import datetime

sel = selectors.DefaultSelector()


class Server:
    def __init__(self, ip: str, port: int, cap=15) -> None:
        self.servsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sel.register(self.servsock, selectors.EVENT_READ, self.add)
        self.servsock.bind((ip, port))
        self.servsock.setblocking(False)
        self.servsock.listen(cap)
        self.clients = []
        self.client_ip = dict()

    def __repr__(self) -> str:
        return "".join(self.clients)

    def run(self):
        while True:
            events = sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    def add(self, sock, mask):
        client_sock, client_ip = self.servsock.accept()
        self.client_ip[client_sock] = client_ip
        client_sock.sendall("\t\t\tWelcome to shitchat!".encode())
        for cs in self.clients:
            cs.sendall(f"\t\t\t {client_ip[0]} {client_ip[1]} has joined us!".encode())
        client_sock.setblocking(False)
        self.clients.append(client_sock)
        sel.register(client_sock, selectors.EVENT_READ, self.read)

    def close(self):
        self.client_ip = dict()
        for client_sock in self.clients:
            client_sock.close()
        self.servsock.close()

    def read(self, conn, mask):
        data = conn.recv(1024)
        if data:
            ip = self.client_ip[conn]
            data = f"By {ip[0]} {ip[1]} {datetime.now()}: ".encode() + data
            print(data.decode().strip())
            for cleint_socket in self.clients:
                if cleint_socket is not conn:
                    cleint_socket.sendall(data.decode().strip().encode())
        else:
            del self.client_ip[conn]
            self.clients.remove(conn)
            sel.unregister(conn)

try: 
    s = Server("localhost", 6666)
    s.run()
except KeyboardInterrupt:
    s.close()