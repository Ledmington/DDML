import pytest

from peers.normal_peer import NormalPeer


def test_dying_peer():
	p = NormalPeer()
	p.die()
	with pytest.raises(Exception):
		p.main_loop()