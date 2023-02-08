# Echo client program
import json
import queue
import socket
import threading
import time

from MelodieInfra.comm.base import recv


class TCPClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.send_queue: "queue.Queue[bytes]" = queue.Queue()
        self.recv_queue: "queue.Queue[bytes]" = queue.Queue()
        self.sending_thread = threading.Thread(target=self.sending_loop)
        self.sending_thread.setDaemon(True)
        self.sending_thread.start()

        self.receiving_thread = threading.Thread(target=self.recv_loop)
        self.receiving_thread.setDaemon(True)
        self.receiving_thread.start()

    @staticmethod
    def _format_bytes(b: bytes):
        return len(b).to_bytes(4, 'little') * 2 + b

    def send_string(self, msg: str):
        self.send_queue.put(msg.encode('utf8'))

    def send_json(self, json_obj):
        self.send_string(json.dumps(json_obj))

    def sending_loop(self):
        while 1:
            item_to_send = self.send_queue.get()
            print('json sent!', item_to_send, self._format_bytes(item_to_send))
            self.sock.sendall(self._format_bytes(item_to_send))

    def recv_loop(self):
        while 1:
            b = recv(self.sock)
            self.recv_queue.put(b)


def create_client():
    client = TCPClient('127.0.0.1', 5006)
    client.send_json({123: 123})
    print('received', client.recv_queue.get())
    while 1:
        time.sleep(1)


if __name__ == "__main__":
    th = threading.Thread(target=create_client)
    th.setDaemon(True)
    th.start()
    th.join()
    # start_tcp_server()
