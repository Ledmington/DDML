import sys
import socket
from datetime import datetime
import logging

from ddml.peers.protocol import Protocol
from ddml.utils.asserts import assert_int
from ddml.utils.worker import Worker
from ddml.utils.colors import ColoredFormatter


class Peer(Worker):
    """
    Peer of the Decentralized Distributed Machine Learning project.
    """

    PORT = 10000
    BUFSIZE = 1024

    def __init__(
        self,
        port=PORT,
        broadcast=True,
        peers=[],
        seconds_wait=5,
        silence_interval=10,
        dead_interval=30,
        log_fmt=ColoredFormatter(),
    ):
        """
        Args:
            port: the port
            broadcast: tells the peer to broadcast
            peers: list of peers
            seconds_wait: the seconds to wait
            silence_interval: time to wait before responding?
            dead_interval: time to wait to declare another peer dead
            log_fmt: formatter for the logger

        Raises:
            TypeError: if port is not an int
            TypeError: if seconds_wait is not an int
            TypeError: if silence_interval is not an int
            TypeError: if dead_interval is not an int
            TypeError: if broadcast is not a bool

            ValueError: if port is less than 0 or more than 65536
            ValueError: if seconds_wait is less or equal to 0
            ValueError: if silence_interval is less or equal to 0
            ValueError: if dead_interval is less or equal to 0
        """

        self.port = assert_int(port, lambda x: 0 < x < 65536)
        self.seconds_to_wait = assert_int(seconds_wait, lambda x: x > 0)
        self.max_seconds_without_answers = assert_int(silence_interval, lambda x: x > 0)
        self.seconds_to_be_dead = assert_int(dead_interval, lambda x: x > 0)

        if type(broadcast) is not bool:
            raise TypeError("Broadcast must be boolean")
        self.broadcast = broadcast

        self.known_peers = dict()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.settimeout(self.seconds_to_wait)
        self.s.bind(("", self.port))

        self.peer_ip = socket.gethostbyname(socket.gethostname())

        self._setup_logger(log_fmt)
        self.logger = logging.getLogger("ddml-peer")

        self.logger.info(f"Peer ready at ({self.peer_ip})")
        Worker.__init__(self, task=self._recv_parse_loop)

    def _broadcast(self, msg: str):
        self.logger.info(f'Broadcasting "{msg}"')
        if self.broadcast is True:
            # TODO: change this address to LAN broadcast
            self.s.sendto(msg.encode(), ("<broadcast>", self.port))

        for peer in self.known_peers:
            self.s.sendto(msg.encode(), (peer, self.port))

    def _setup_logger(self, console_fmt=ColoredFormatter()):
        # create logs directory
        # if not os.path.exists("logs"):
        #    os.mkdir("logs")

        self.logger = logging.getLogger("ddml-peer")
        self.logger.setLevel(logging.INFO)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(console_fmt)
        self.logger.addHandler(stdout_handler)

        # file_handler = logging.FileHandler("logs/ddml-peer.log")
        # file_handler.setLevel(logging.DEBUG)
        # formatter = logging.Formatter(
        #    "[%(asctime)s][%(levelname)s]: %(message)s", "%m-%d-%Y %H:%M:%S"
        # )
        # file_handler.setFormatter(formatter)
        # logger.addHandler(file_handler)

    def is_alive(self):
        """
        TODO
        """

        return self.s is not None and Worker.is_alive(self)

    def _assert_alive(self):
        if not self.is_alive():
            raise ValueError

    def _parse_request(self, msg, address):
        if address == self.peer_ip:
            return

        # Updating last_response
        self.known_peers[address] = datetime.now()

        self.logger.info(f'Received message "{msg}" from address "{address}"')

        if msg == Protocol.NEW_MSG:
            self.logger.info(f"A new peer has joined the network ({address})")
        elif msg == Protocol.LEAVE_MSG:
            self.logger.info(f"A peers has leaved the network ({address})")
            self.known_peers.remove(address)
        elif msg == Protocol.HELLO_MSG:
            self.logger.info(f"Received hello packet from {address}")
            self.s.sendto(Protocol.ALIVE_MSG.encode(), (address, self.port))
        elif msg == Protocol.ALIVE_MSG:
            # Do nothing (because we already updated its last response)
            pass
        else:
            self.logger.critical("Unknown message")
            raise ValueError("Unknown message")

    def _check_dead_peers(self):
        for (address, last_response) in self.known_peers.copy().items():
            time_passed = (datetime.now() - last_response).seconds
            if time_passed >= self.seconds_to_be_dead:
                # This peer is considered dead
                self.logger.warning(f"{address} is dead")
                del self.known_peers[address]
            elif time_passed >= self.max_seconds_without_answers:
                self.logger.warning(f"Long time no news from {address}")
                self.s.sendto(Protocol.HELLO_MSG.encode(), (address, self.port))

    def _recv_parse_loop(self):
        self.logger.info(f"I know {len(self.known_peers)} other peers")
        try:
            msg, address = self.s.recvfrom(Peer.BUFSIZE)
            self._parse_request(msg.decode(), address[0])
        except socket.timeout:
            self.logger.info(f"{self.seconds_to_wait} seconds without answer")
            self._check_dead_peers()

    def start(self):
        """
        TODO
        """

        if self.is_alive() is True:
            raise RuntimeError("Cannot start an already alive Peer")
        if Worker.is_shutdown(self) is True:
            raise RuntimeError("Cannot start a dying Peer")
        self._broadcast(Protocol.NEW_MSG)
        Worker.start(self)
        self.logger.info(f"Peer started at {self.peer_ip}")

    def die(self):
        """
        TODO
        """

        self.logger.info("Shutting down")
        Worker.die(self)

    def join(self, timeout=None):
        """
        TODO
        """

        self.logger.info("Waiting for the peer to die")
        Worker.join(self, timeout)
        self.logger.info(f'Broadcasting "{Protocol.LEAVE_MSG:s}"')
        if self.s is not None:
            self._broadcast(Protocol.LEAVE_MSG)
            self.s.close()
            self.s = None
        self.logger.info("Peer dead")
