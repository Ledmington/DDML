from ddml.peers.dead.dead_peer import DeadPeer


def test_dies_automatically():
    p = DeadPeer()
    p.main_loop()
    assert p.alive is False
