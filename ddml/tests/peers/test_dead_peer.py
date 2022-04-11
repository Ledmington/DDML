import socket
from ddml.peers.dead.dead_peer import DeadPeer


def test_dies_automatically():
    p = DeadPeer()
    p.main_loop()
    assert p.alive is False


def test_allowed_messages():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(1)
    s.bind(("", 10000))
    p = DeadPeer()
    p.main_loop()

    msg, address = s.recvfrom(1024)
    assert msg.decode() == "new"
