import os
import pytest
from testcontainers.compose import DockerCompose
from testcontainers.core.waiting_utils import wait_for_logs

from ddml import ROOT_DIR


@pytest.mark.skip  # uncomment to avoid slow integration testing
def test_one_dead_peer():
    compose_file = "test_one_dead_peer.yml"

    with DockerCompose(
        os.sep.join([ROOT_DIR, "tests", "peers"]), compose_file_name=compose_file
    ) as compose:
        try:
            wait_for_logs(compose, "is dead", timeout=120)
        except TimeoutError:
            pytest.fail()
