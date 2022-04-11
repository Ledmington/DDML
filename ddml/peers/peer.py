import socket
from datetime import datetime

from ddml.peers.protocol import Protocol
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
        if self.alive is False:
            raise ValueError

    def parse_request(self, msg, address):
        if address == self.peer_ip:
            return

        # Updating last_response
        self.known_peers[address] = datetime.now()

        if msg == Protocol.NEW_MSG:
            print(f"A new peer has joined the network ({address})")
        # elif msg == "bye":
        #    print(f"A peers has leaved the network ({address})")
        #    known_peers.remove(address)
        elif msg == Protocol.HELLO_MSG:
            print(f"Received hello packet from {address}")
            self.s.sendto(Protocol.ALIVE_MSG, (address, self.port))
        elif msg == Protocol.ALIVE_MSG:
            # Do nothing (because we already updated its last response)
            pass
        else:
            raise Exception("Unknown message")

    def check_dead_peers(self):
        for (address, last_response) in self.known_peers.copy().items():
            time_passed = (datetime.now() - last_response).seconds
            if time_passed >= self.seconds_to_be_dead:
                # This peer is considered dead
                print(f"{address} is dead")
                del self.known_peers[address]
            elif time_passed >= self.max_seconds_without_answers:
                print(f"Long time no news from {address}")
                self.s.sendto(Protocol.HELLO_MSG, (address, self.port))

    def main_loop(self):
        self._assert_alive()
        print(f"Peer started ({self.peer_ip})...")

        self.s.sendto(Protocol.NEW_MSG, ("<broadcast>", self.port))

        while True:
            print(f"I know {len(self.known_peers)} other peers")
            try:
                msg, address = self.s.recvfrom(self.bufsize)
                self.parse_request(msg.decode(), address[0])
            except socket.timeout:
                print(f"{self.seconds_to_wait} seconds without answer")
                self.check_dead_peers()

    def die(self):
        self._assert_alive()
        self.s.close()
        self.alive = False


if __name__ == "__main__":
    p = Peer()
    p.main_loop()
