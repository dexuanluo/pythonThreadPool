import socket
from threadpool.pool import ThreadPool as tp
from threadpool.task import Task

class ProcessTask(Task):
    def __init__(self, packet, *args, **kwargs):
        self.packet = packet
        Task(func = self.process, *args, **kwargs)
    def process(self):
        pass

class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        self.ip = "192.168.1.113"
        self.port = 8888
        self.socket.bind((self.socket, self.port))

        self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        self.pool = tp(10)
    def loop_server(self):
        while True:
            packet, address = self.socket.rev(65535)
            task = ProcessTask(paccket)
            result = task.get_
