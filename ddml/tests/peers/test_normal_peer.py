import pytest
from ddml.peers.normal.normal_peer import NormalPeer


def test_cannot_start_dead_peer():
    p = NormalPeer()
    p.die()
    with pytest.raises(Exception):
        p.main_loop()
