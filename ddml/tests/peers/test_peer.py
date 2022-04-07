import pytest

from ddml.peers.peer import Peer


def test_peer_initially_alive():
    p = Peer()
    p._assert_alive()


def test_peer_can_die():
    p = Peer()
    p.die()
    with pytest.raises(ValueError):
        p._assert_alive()


def test_peer_cant_die_twice():
    p = Peer()
    p.die()
    with pytest.raises(ValueError):
        p.die()


def test_port_is_int():
    for x in [None, "abc", 1.5, [], (), dict(), set()]:
        with pytest.raises(TypeError):
            p = Peer(port=x)


def test_port_is_valid():
    for x in [-1, 0, 65536]:
        with pytest.raises(ValueError):
            p = Peer(port=x)


def test_bufsize_is_int():
    for x in [None, "abc", 1.5, [], (), dict(), set()]:
        with pytest.raises(TypeError):
            p = Peer(bufsize=x)


def test_bufsize_is_valid():
    for x in [-1, 0]:
        with pytest.raises(ValueError):
            p = Peer(bufsize=x)


def test_wait_is_int():
    for x in [None, "abc", 1.5, [], (), dict(), set()]:
        with pytest.raises(TypeError):
            p = Peer(seconds_wait=x)


def test_wait_is_valid():
    for x in [-1, 0]:
        with pytest.raises(ValueError):
            p = Peer(seconds_wait=x)


def test_interval_is_int():
    for x in [None, "abc", 1.5, [], (), dict(), set()]:
        with pytest.raises(TypeError):
            p = Peer(silence_interval=x)


def test_interval_is_valid():
    for x in [-1, 0]:
        with pytest.raises(ValueError):
            p = Peer(silence_interval=x)


def test_dead_interval_is_int():
    for x in [None, "abc", 1.5, [], (), dict(), set()]:
        with pytest.raises(TypeError):
            p = Peer(dead_interval=x)


def test_dead_interval_is_valid():
    for x in [-1, 0]:
        with pytest.raises(ValueError):
            p = Peer(dead_interval=x)
