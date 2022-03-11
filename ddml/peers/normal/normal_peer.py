import socket
import random
import time
from datetime import datetime

from ddml.peers.peer import Peer


class NormalPeer(Peer):
	def __init__(self):
		Peer.__init__(self)
		time.sleep(random.uniform(0, 5))

	def parse_request(self, msg, address):
		if address == self.peer_ip:
			return

		# Updating last_response
		self.known_peers[address] = datetime.now()

		if msg == "new":
			print(f"A new peer has joined the network ({address})")
		# elif msg == "bye":
		#    print(f"A peers has leaved the network ({address})")
		#    known_peers.remove(address)
		elif msg == "hello":
			print(f"Received hello packet from {address}")
			self.s.sendto("alive".encode(), (address, self.port))
		elif msg == "alive":
			# Do nothing (because we already updated its last response)
			pass
		else:
			raise Exception("Unknown message")

	def check_dead_peers(self):
		for (address, last_response) in self.known_peers.copy().items():
			time_passed = (datetime.now() - last_response).seconds
			if time_passed >= self.seconds_to_be_dead:
				# This peers is considered dead
				print(f"{address} is dead")
				del self.known_peers[address]
			elif time_passed >= self.max_seconds_without_answers:
				print(f"Long time no news from {address}")
				self.s.sendto("hello".encode(), (address, self.port))

	def main_loop(self):
		self._assert_alive()
		print(f"Peer started ({self.peer_ip})...")

		self.s.sendto("new".encode(), ("<broadcast>", self.port))

		while True:
			print(f"I know {len(self.known_peers)} other peers")
			try:
				msg, address = self.s.recvfrom(self.bufsize)
				self.parse_request(msg.decode(), address[0])
			except socket.timeout:
				print(f"{self.seconds_to_wait} seconds without answer")
				self.check_dead_peers()


if __name__ == "__main__":
	p = NormalPeer()
	p.main_loop()
