import socket


class Peer:
    def __init__(self,
                 port=10000,
                 bufsize=1024,
                 seconds_wait=5,
                 silence_interval=10,
                 dead_interval=30):
        self.known_peers = dict()
        self.port = port
        self.bufsize = bufsize
        self.seconds_to_wait = seconds_wait
        self.max_seconds_without_answers = silence_interval
        self.seconds_to_be_dead = dead_interval

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
