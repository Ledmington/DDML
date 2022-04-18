import pytest

from ddml.peers.peer import Peer


def test_peer_initially_dead():
    p = Peer()
    assert p.is_alive() is False


def test_peer_can_die():
    p = Peer()
    p.die()
    with pytest.raises(ValueError):
        p._assert_alive()


def test_peer_can_die_twice():
    p = Peer()
    p.die()
    p.die()


def test_cannot_start_dead_peer():
    p = Peer()
    p.die()
    with pytest.raises(RuntimeError):
        p.start()


def test_peer_is_alive_after_start():
    p = Peer()
    p.start()
    assert p.is_alive() is True
    p.join()


def test_peer_cant_start_twice():
    p = Peer()
    p.start()
    with pytest.raises(RuntimeError):
        p.start()
    p.join()


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
