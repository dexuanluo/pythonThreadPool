import socket
import fcntl
from threadpool.pool import ThreadPool as tp
from threadpool.task import AsyncTask
import json

class ProcessTask(AsyncTask):
    def __init__(self, packet, *args, **kwargs):
        self.packet = packet
        super().__init__(func = self.process, *args, **kwargs)
    def process(self):
        pass

class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, \
            socket.IPPROTO_IP)
        self.ip = "192.168.1.113"
        self.port = 8888
        self.socket.bind((self.ip, self.port))
        fcntl.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        self.pool = tp(10)

    def loop_server(self):
        while True:
            packet, address = self.socket.recv(65535)
            item = ProcessTask(packet)
            self.pool.put(item)
            result = item.get_result()
            result = json.dumps(result, indent = 4)
            print(result)
if __name__ == "__main__":
    server = Server()
    server.loop_server()
