import socket
import pickle
from constants import SERVER_IP, SERVER_PORT

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (SERVER_IP, SERVER_PORT)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except Exception as e:
            print("Error in connection")
            print("Error:", e)
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            # print(self.client.recv(2048).decode())
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)
