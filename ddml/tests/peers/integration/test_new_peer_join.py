import os
import time
from testcontainers.compose import DockerCompose

from ddml import ROOT_DIR


# @pytest.mark.skip  # uncomment to avoid slow integration testing
def test_one_dead_peer():
    compose_file = "test_new_peer_join.yml"

    with DockerCompose(
        os.sep.join([ROOT_DIR, "tests", "peers", "integration"]),
        compose_file_name=compose_file,
    ) as compose:
        time.sleep(30)
        stdout, stderr = compose.get_logs()

    lines = stdout.decode().split("\n")
    normal_peer_log = filter(lambda s: "normal" in s, lines)
    delayed_peer_log = filter(lambda s: "delayed" in s, lines)

    assert any(["1 other" in s for s in normal_peer_log])
    assert any(["1 other" in s for s in delayed_peer_log])
