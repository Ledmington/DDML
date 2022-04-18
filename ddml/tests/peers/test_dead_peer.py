import socket
import pytest

from ddml.peers.dead.dead_peer import DeadPeer
from ddml.peers.protocol import Protocol


def test_initially_dead():
    p = DeadPeer()
    assert p.is_alive() is False


def test_dies_automatically():
    p = DeadPeer()
    p.start()
    assert p.is_alive() is False


def test_cannot_call_start_twice():
    p = DeadPeer()
    p.start()
    with pytest.raises(RuntimeError):
        p.start()


def test_allowed_messages():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(1)
    s.bind(("", 10000))
    p = DeadPeer()
    p.start()

    msg, address = s.recvfrom(1024)
    assert msg == Protocol.NEW_MSG

    s.close()


def test_cannot_call_parse_request():
    p = DeadPeer()
    with pytest.raises(Exception):
        p.parse_request()


def test_cannot_call_check_dead_peers():
    p = DeadPeer()
    with pytest.raises(Exception):
        p.check_dead_peers()
