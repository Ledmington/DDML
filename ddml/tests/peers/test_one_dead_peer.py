import os
from testcontainers.compose import DockerCompose
from testcontainers.core.waiting_utils import wait_for_logs

from ddml import ROOT_DIR
from ddml.peers.peer import Peer


def test_one_dead_peer():
    p = Peer()  # TODO: change this code in order to read simple constants
    time_to_wait = p.seconds_to_be_dead + p.max_seconds_without_answers
    p.die()

    compose_file = "test_one_dead_peer.yml"

    with DockerCompose(
        os.sep.join([ROOT_DIR, "tests", "peers"]), compose_file_name=compose_file
    ) as compose:
        wait_for_logs(compose, r".* is dead")
