import json
import queue
import threading

from flask import Flask
from flask_sock import Sock, Server, ConnectionClosed as WSClosed
from typing import List, Set


def create_visualizer_server(recv_queue: queue.Queue, send_queue: queue.Queue):
    app = Flask(__name__)
    sock = Sock(app)
    websockets: List[Server] = []

    def send():
        while 1:
            try:
                data = send_queue.get(timeout=1)
                closed_websockets: Set[int] = set()
                for websocket in websockets:
                    try:
                        websocket.send(data)
                    except WSClosed:
                        closed_websockets.add(id(websocket))
                        pass
                for ws_index in range(len(websockets) - 1, 0, -1):
                    if id(websockets[ws_index]) in closed_websockets:
                        websockets.pop(ws_index)
            except queue.Empty:
                pass

    thread_send = threading.Thread(target=send)
    thread_send.setDaemon(True)
    thread_send.start()

    @sock.route('/echo')
    def echo(ws: Server):
        websockets.append(ws)
        while True:
            try:
                content = ws.receive()
                rec = json.loads(content)
                cmd = rec["cmd"]
                data = rec["data"]
                if 0 <= cmd <= 10:
                    try:
                        recv_queue.put((cmd, data), timeout=1)
                    except:
                        import traceback
                        traceback.print_exc()
                else:
                    raise NotImplementedError(cmd)


            except json.JSONDecodeError:
                import traceback
                traceback.print_exc()

    app.run(host='0.0.0.0', port=8765)
