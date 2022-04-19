import socket
from datetime import datetime

from ddml.peers.protocol import Protocol
from ddml.utils.asserts import assert_int
from ddml.utils.worker import Worker


class Peer(Worker):
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

        print(f"Peer ready at ({self.peer_ip})...")
        Worker.__init__(self, task=self._recv_parse_loop)

    def is_alive(self):
        return self.s is not None and Worker.is_alive(self)

    def _assert_alive(self):
        if not self.is_alive():
            raise ValueError

    def _parse_request(self, msg, address):
        if address == self.peer_ip:
            return

        # Updating last_response
        self.known_peers[address] = datetime.now()

        print(f'Received message "{msg}" from address "{address}"')

        if msg == Protocol.NEW_MSG:
            print(f"A new peer has joined the network ({address})")
        elif msg == Protocol.LEAVE_MSG:
            print(f"A peers has leaved the network ({address})")
            self.known_peers.remove(address)
        elif msg == Protocol.HELLO_MSG:
            print(f"Received hello packet from {address}")
            self.s.sendto(Protocol.ALIVE_MSG.encode(), (address, self.port))
        elif msg == Protocol.ALIVE_MSG:
            # Do nothing (because we already updated its last response)
            pass
        else:
            raise ValueError("Unknown message")

    def _check_dead_peers(self):
        for (address, last_response) in self.known_peers.copy().items():
            time_passed = (datetime.now() - last_response).seconds
            if time_passed >= self.seconds_to_be_dead:
                # This peer is considered dead
                print(f"{address} is dead")
                del self.known_peers[address]
            elif time_passed >= self.max_seconds_without_answers:
                print(f"Long time no news from {address}")
                self.s.sendto(Protocol.HELLO_MSG.encode(), (address, self.port))

    def _recv_parse_loop(self):
        print(f"I know {len(self.known_peers)} other peers")
        try:
            msg, address = self.s.recvfrom(self.bufsize)
            self._parse_request(msg.decode(), address[0])
        except socket.timeout:
            print(f"{self.seconds_to_wait} seconds without answer")
            self._check_dead_peers()

    def start(self):
        if self.is_alive() is True:
            raise RuntimeError("Cannot start an already alive Peer")
        if Worker.is_shutdown(self) is True:
            raise RuntimeError("Cannot start a dying Peer")
        self.s.sendto(Protocol.NEW_MSG.encode(), ("<broadcast>", self.port))
        Worker.start(self)
        print(f"Peer started at {self.peer_ip}")

    def die(self):
        Worker.die(self)

    def join(self):
        print("Waiting for the peer to die")
        Worker.join(self)
        print(f'Broadcasting "{Protocol.LEAVE_MSG}"')
        if self.s is not None:
            self.s.sendto(Protocol.LEAVE_MSG.encode(), ("<broadcast>", self.port))
            self.s.close()
            self.s = None
        print("Peer dead")


if __name__ == "__main__":
    p = Peer()
    p.start()
    p.join()
