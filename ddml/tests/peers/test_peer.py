import pytest

from ddml.peers.peer import Peer


def test_peer_initially_dead():
    w = Peer()
    assert w.is_shutdown() is False
    assert w.is_alive() is False


def test_when_started_is_alive():
    w = Peer()
    w.start()
    assert w.is_shutdown() is False
    assert w.is_alive() is True
    w.die()
    w.join()


def test_cant_start_twice():
    w = Peer()
    w.start()
    with pytest.raises(RuntimeError):
        w.start()
    w.die()
    w.join()


def test_cannot_start_dead_peer():
    w = Peer()
    w.start()
    w.die()
    with pytest.raises(RuntimeError):
        w.start()
    w.join()


def test_cannot_start_joined_peer():
    w = Peer()
    w.start()
    w.die()
    w.join()
    with pytest.raises(RuntimeError):
        w.start()


def test_is_shutdown_after_die():
    w = Peer()
    w.start()
    w.die()
    assert w.is_shutdown() is True
    w.join()


def test_is_dead_after_join():
    w = Peer()
    w.start()
    w.die()
    w.join()
    assert w.is_shutdown() is True
    assert w.is_alive() is False


def test_can_die_twice():
    w = Peer()
    w.start()
    w.die()
    w.die()
    w.join()


def test_can_join_twice():
    w = Peer()
    w.start()
    w.die()
    w.join()
    w.join()


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
