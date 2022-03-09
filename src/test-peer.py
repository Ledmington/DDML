import unittest

from peer.normal_peer import NormalPeer

class TestPeer(unittest.TestCase):
	def test_dying_peer(self):
		p = NormalPeer()
		p.die()
		self.assertRaises(Exception, lambda: p.main_loop())

if __name__ == "__main__":
	unittest.main()