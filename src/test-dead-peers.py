import unittest
import os
import time
from testcontainers.compose import DockerCompose

from peer.peer import Peer


class TestDeadPeers(unittest.TestCase):
	compose_file = os.sep.join(["src", "test-dead-peer.yml"])

	def setUp(self):
		pass

	def test_one_dead_peer(self):
		p = Peer()
		time_to_wait = p.seconds_to_be_dead + p.max_seconds_without_answers
		p.die()
		p = None

		stdout, stderr = None, None

		with DockerCompose(".",
						compose_file_name=[self.compose_file],
						pull=True) as compose:
			time.sleep(time_to_wait)
			stdout, stderr = compose.get_logs()
			if stderr:
				print(stderr)
				self.fail()

		lines = stdout.decode("utf-8").split("\r\n")
		lines = list(filter(lambda s: s.startswith("peer"), lines))
		message = list(filter(lambda s: s.endswith(" is dead"), lines))
		self.assertEqual(len(message), 1, "stdout: " + stdout.decode("utf-8"))


if __name__ == "__main__":
	unittest.main()
