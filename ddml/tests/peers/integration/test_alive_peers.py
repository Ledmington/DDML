import os
import pytest
from testcontainers.compose import DockerCompose
from testcontainers.core.waiting_utils import wait_for_logs

from ddml import ROOT_DIR


# @pytest.mark.skip  # uncomment to avoid slow integration testing
def test_alive_peers():
    compose_file = "test_alive_peers.yml"

    with DockerCompose(
        os.sep.join([ROOT_DIR, "tests", "peers", "integration"]),
        compose_file_name=compose_file,
    ) as compose:
        try:
            wait_for_logs(compose, "is dead", timeout=120)
        except TimeoutError:
            pytest.fail()
