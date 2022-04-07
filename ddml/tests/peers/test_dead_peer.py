def test_dies_automatically():
    from ddml.peers.dead.dead_peer import DeadPeer

    p = DeadPeer()
    p.main_loop()
    assert p.alive is False
