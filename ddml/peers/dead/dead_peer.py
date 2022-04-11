from ddml.peers.peer import Peer
from ddml.peers.protocol import Protocol


class DeadPeer(Peer):
    def __init__(self):
        Peer.__init__(self)
        self.parse_request = None
        self.check_dead_peers = None

    def main_loop(self):
        self._assert_alive()
        print(f"Peer started ({self.peer_ip})...")
        self.s.sendto(Protocol.NEW_MSG, ("<broadcast>", self.port))
        self.die()
        print("Peer dead")


if __name__ == "__main__":
    p = DeadPeer()
    p.main_loop()
