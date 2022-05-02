"""
This module contains the Peer class, core of the DDML project.
"""

import sys
import socket
from datetime import datetime
import logging

from ddml.peers.protocol import Protocol
from ddml.utils.asserts import assert_int
from ddml.utils.worker import Worker
from ddml.utils.colors import ColoredFormatter

# pylint: disable=too-many-instance-attributes
class Peer(Worker):
    """
    Peer of the Decentralized Distributed Machine Learning project.
    """

    PORT = 10000
    BUFSIZE = 1024

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        port=PORT,
        broadcast=True,
        peers=None,
        seconds_wait=5,
        silence_interval=10,
        dead_interval=30,
        log_fmt=ColoredFormatter(),
    ):
        """
        Creates a Peer without making it start.

        Args:
            port: the port
            broadcast: tells the peer to broadcast in the LAN
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

        if not isinstance(broadcast, bool):
            raise TypeError("Broadcast must be boolean")
        self.broadcast = broadcast

        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.peer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.peer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.peer_socket.settimeout(self.seconds_to_wait)
        self.peer_socket.bind(("", self.port))

        self.peer_ip = socket.gethostbyname(socket.gethostname())

        self._setup_logger(log_fmt)
        self.logger = logging.getLogger("ddml-peer")

        self.logger.info("Peer ready at (%s)", self.peer_ip)
        Worker.__init__(self, task=self._recv_parse_loop)

        self.known_peers = {}
        if peers is not None:
            for peer_address in peers:
                self.logger.info('Adding "%s" to the list of known peers', peer_address)
                self.known_peers[peer_address] = datetime.now()

    def _broadcast(self, msg: str):
        self.logger.info('Broadcasting "%s"', msg)
        if self.broadcast is True:
            self.peer_socket.sendto(msg.encode(), ("255.255.255.255", self.port))

        for peer in self.known_peers:
            self.peer_socket.sendto(msg.encode(), (peer, self.port))

    def _setup_logger(self, console_fmt=ColoredFormatter()):

        self.logger = logging.getLogger("ddml-peer")
        self.logger.setLevel(logging.INFO)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(console_fmt)
        self.logger.addHandler(stdout_handler)

    def is_alive(self):
        """
        TODO
        """

        return self.peer_socket is not None and Worker.is_alive(self)

    def _assert_alive(self):
        if not self.is_alive():
            raise ValueError

    def _parse_request(self, msg, address):
        if address == self.peer_ip:
            return

        # Updating last_response
        self.known_peers[address] = datetime.now()

        self.logger.info('Received message "%s" from address "%s"', msg, address)

        if msg == Protocol.NEW_MSG:
            self.logger.info("A new peer has joined the network (%s)", address)
        elif msg == Protocol.LEAVE_MSG:
            self.logger.info("A peers has leaved the network (%s)", address)
            self.known_peers.pop(address)
        elif msg == Protocol.HELLO_MSG:
            self.logger.info('Answering with "%s"', Protocol.ALIVE_MSG)
            self.peer_socket.sendto(Protocol.ALIVE_MSG.encode(), (address, self.port))
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
                self.logger.warning("%s is dead", address)
                del self.known_peers[address]
            elif time_passed >= self.max_seconds_without_answers:
                self.logger.warning("Long time no news from %s", address)
                self.peer_socket.sendto(
                    Protocol.HELLO_MSG.encode(), (address, self.port)
                )

    def _recv_parse_loop(self):
        self.logger.info("I know %d other peers", len(self.known_peers))
        try:
            msg, address = self.peer_socket.recvfrom(Peer.BUFSIZE)
            self._parse_request(msg.decode(), address[0])
        except socket.timeout:
            self.logger.info("%d seconds without answer", self.seconds_to_wait)
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
        self.logger.info("Peer started at %s", self.peer_ip)

    def die(self):
        """
        Shuts down the Peer.

        This is a non-blocking call. To wait for Peer's termination, use join().
        """

        self.logger.info("Shutting down")
        Worker.die(self)

    def join(self, timeout=None):
        """
        Waits for the Peer to terminate and broadcasts the LEAVE_MSG defined in the Protocol.

        Args:
            timeout: an optional float representing the maximum number of seconds to wait.
                To check if a timeout occurred, you should call is_alive after join.
                If timeout is not given, this method waits undefinitely.
        """

        self.logger.info("Waiting for the peer to die")
        Worker.join(self, timeout)
        self.logger.info('Broadcasting "%s"', Protocol.LEAVE_MSG)
        if self.peer_socket is not None:
            self._broadcast(Protocol.LEAVE_MSG)
            self.peer_socket.close()
            self.peer_socket = None
        self.logger.info("Peer dead")
