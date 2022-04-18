from ddml.peers.peer import Peer
from ddml.peers.protocol import Protocol


class DeadPeer(Peer):
    def __init__(self):
        Peer.__init__(self)
        self.parse_request = None
        self.check_dead_peers = None
        self.called = False

    def is_alive(self):
        return False

    def start(self):
        if self.called is True:
            raise RuntimeError
        self.called = True
        print(f"Peer started ({self.peer_ip})")
        self.s.sendto(Protocol.NEW_MSG, ("<broadcast>", self.port))
        self.die()
        print("Peer dead")


if __name__ == "__main__":
    p = DeadPeer()
    p.start()
