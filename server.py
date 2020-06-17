import socket

s = socket.socket(socket.AF_INET, socket.SOCK_RAW)
s.bind((socket.gethostname(), 1234))
s.listen(10)
while True:
    client, address = s.accept()
    print(f"listening from {address}")
    print("request recieved")
    msg = input()
    client.send(bytes(msg, "utf-8"))
    client.close()
