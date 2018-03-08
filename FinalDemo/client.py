import socket
import time
import sys

class RaspConnection():
    def __init__(self, ip = "108.179.188.43", port=8888):
        #RPi's IP
        self.SERVER_IP = ip
        self.SERVER_PORT = port

        print("Starting socket: TCP...")
        self.server_addr = (self.SERVER_IP, self.SERVER_PORT)
        self.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        while True:
            try:
                print("Connecting to server @ %s:%d..." %(self.SERVER_IP, self.SERVER_PORT))
                self.socket_tcp.connect(self.server_addr)
                break
            except Exception:
                print("Can't connect to server,try it latter!")
                time.sleep(1)
                continue

    #o for stop, 1 for start, 2 for think, 3 for
    def send_commands(self, command):
        data = self.socket_tcp.recv(512)
        if len(data) > 0:
            print("Received: %s" % data)
            # command=input()
            self.socket_tcp.send(command.encode())
            time.sleep(1)
        # while True:
        #     try:
        #
        #             continue
        #     except Exception:
        #         self.socket_tcp.close()
        #         socket_tcp=None
        #         sys.exit(1)

if __name__ == '__main__':
    cnt = RaspConnection()
    cnt.connect()
    cnt.send_commands('1')
    time.sleep(5)

    cnt.send_commands('2')
    time.sleep(5)
    cnt.send_commands('3')
    time.sleep(5)

    cnt.send_commands('4')
    time.sleep(5)