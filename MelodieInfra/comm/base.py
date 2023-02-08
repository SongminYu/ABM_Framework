import socket


def format_bytes(b: bytes):
    byts = len(b).to_bytes(4, 'little') * 2 + b
    return byts


def recv(conn: socket.socket):
    data = conn.recv(8)
    if not data:
        return
    # Receive head
    length1 = int.from_bytes(data[:4], 'little')
    length2 = int.from_bytes(data[4:], 'little')

    assert length1 == length2, (length1, length2)
    length = length1
    request_strs = []

    # Receive the payload
    times = length // 4096
    tail_len = length % 4096
    print('length', length1, length2, times, tail_len)
    for i in range(times):
        data = conn.recv(4096)
        if not data:
            return
        request_strs.append(data)
    data = conn.recv(tail_len)
    print('data', data)
    if not data:
        return
    request_strs.append(data)
    return b"".join(request_strs)
