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
