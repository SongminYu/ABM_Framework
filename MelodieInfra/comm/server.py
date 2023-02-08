import logging
import socket
import threading
import time
from typing import List
from MelodieInfra.comm.base import recv, format_bytes

STATUS_IDLE = 0
STATUS_LENGTH_PARSED = 1
logger = logging.getLogger(__name__)


def connection_loop(conn: socket.socket):
    while 1:
        request = recv(conn)
        if not request:
            return
        conn.send(format_bytes(request))  # echo


def start_tcp_server():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5006

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    while 1:
        try:
            conn, addr = s.accept()
            connection_loop(conn)
            conn.close()
        except AssertionError as e:
            import traceback
            traceback.print_exc()
            logger.error("Illegal TCP message format!")
        except KeyboardInterrupt:
            s.close()


if __name__ == "__main__":
    th = threading.Thread(target=start_tcp_server)
    th.setDaemon(True)
    th.start()
    while 1:
        time.sleep(1)
    # start_tcp_server()
