"""
A module that contains the DeadPeer class.

This is used only for internal testing.
"""

from ddml.peers.peer import Peer
from ddml.peers.protocol import Protocol


class DeadPeer(Peer):
    """
    Class that represents a Peer that terminates tìright after having started.

    This class is used only for internal testing.
    """

    def __init__(self):
        Peer.__init__(self)
        self.parse_request = None
        self.check_dead_peers = None
        self._assert_alive = None
        self._loop = None
        self.called = False

    def is_alive(self):
        return False

    def start(self):
        if self.called is True:
            raise RuntimeError
        self.called = True
        print(f"Peer started ({self.peer_ip})")
        self._broadcast(Protocol.NEW_MSG)
        print("Peer dead")

    def die(self):
        pass

    def join(self, timeout=None):
        pass


if __name__ == "__main__":
    p = DeadPeer()
    p.start()
    p.join()
