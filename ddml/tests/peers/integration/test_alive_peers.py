import os
import time
from testcontainers.compose import DockerCompose

from ddml import ROOT_DIR


# @pytest.mark.skip  # uncomment to avoid slow integration testing
def test_alive_peers():
    compose_file = "test_alive_peers.yml"

    n_peers = 4

    with DockerCompose(
        os.sep.join([ROOT_DIR, "tests", "peers", "integration"]),
        compose_file_name=compose_file,
    ) as compose:
        time.sleep(60)
        stdout, stderr = compose.get_logs()

    lines = stdout.decode().split("\n")
    peers_logs = (
        filter(lambda s: "peer-" + str(i + 1) in s, lines) for i in range(n_peers)
    )

    for log in peers_logs:
        assert 0 < len([filter(lambda s: str(n_peers - 1) + " other peers", log)])
