import os
import time
import pytest
from testcontainers.compose import DockerCompose

from ddml import ROOT_DIR
from ddml.peers.peer import Peer


def test_one_dead_peer():
	p = Peer()  # TODO: change this code in order to read simple constants
	time_to_wait = p.seconds_to_be_dead + p.max_seconds_without_answers
	p.die()

	compose_file = "test_one_dead_peer.yml"

	with DockerCompose(os.sep.join([ROOT_DIR, "tests", "peers"]),
					   compose_file_name=[compose_file],
					   pull=True) as compose:
		time.sleep(time_to_wait)
		stdout, stderr = compose.get_logs()
		if stderr:
			print(stderr)
			pytest.fail()

	lines = stdout.decode("utf-8").split("\r\n")
	lines = list(filter(lambda s: s.startswith("peer"), lines))
	message = list(filter(lambda s: s.endswith(" is dead"), lines))
	assert len(message) == 1
