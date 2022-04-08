import socket

from ddml.utils.asserts import assert_int


class Peer:
    PORT = 10000
    BUFSIZE = 1024

    def __init__(
        self,
        port=PORT,
        bufsize=BUFSIZE,
        seconds_wait=5,
        silence_interval=10,
        dead_interval=30,
    ):
        self.port = assert_int(port, lambda x: 0 < x < 65536)
        self.bufsize = assert_int(bufsize, lambda x: x > 0)
        self.seconds_to_wait = assert_int(seconds_wait, lambda x: x > 0)
        self.max_seconds_without_answers = assert_int(silence_interval, lambda x: x > 0)
        self.seconds_to_be_dead = assert_int(dead_interval, lambda x: x > 0)

        self.known_peers = dict()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.settimeout(self.seconds_to_wait)
        self.s.bind(("", self.port))

        self.peer_ip = socket.gethostbyname(socket.gethostname())

        self.alive = True

    def _assert_alive(self):
        if not self.alive:
            raise ValueError("peer is not alive")

    def parse_request(self, msg: str, address: str):
        pass

    def check_dead_peers(self):
        pass

    def main_loop(self):
        pass

    def die(self):
        self._assert_alive()
        self.s.close()
        self.alive = False
