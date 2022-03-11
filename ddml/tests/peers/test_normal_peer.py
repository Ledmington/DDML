import pytest


def test_cannot_start_dead_peer():
	from ddml.peers.normal.normal_peer import NormalPeer
	p = NormalPeer()
	p.die()
	with pytest.raises(Exception):
		p.main_loop()
