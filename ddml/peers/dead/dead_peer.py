from ddml.peers.peer import Peer


class DeadPeer(Peer):
	def main_loop(self):
		self._assert_alive()
		print(f"Peer started ({self.peer_ip})...")
		self.s.sendto("new".encode(), ("<broadcast>", self.port))
		self.die()
		print("Peer dead")


if __name__ == "__main__":
	p = DeadPeer()
	p.main_loop()
