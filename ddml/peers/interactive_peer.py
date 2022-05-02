"""
This module contains the InteractivePeer class, a wrapper of the Peer class
which allows the user to directly control it.
"""

import logging
from pynput.keyboard import Listener

from ddml.peers.peer import Peer
from ddml.utils.colors import ColoredFormatter


class InteractivePeer(Peer):
    """
    Interactive version of Peer.
    """

    class _CustomFormatter(ColoredFormatter):
        erase_one_line = "\033[1A\033[K"
        commands_bar = "[S]top | [L]ist | [T]rain"

        def format(self, record):
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            return (
                self.erase_one_line
                + formatter.format(record)
                + "\n"
                + self.commands_bar
            )

    def __init__(self, port=Peer.PORT, broadcast=True, peers=None):
        Peer.__init__(self, port, broadcast, peers, log_fmt=self._CustomFormatter())
        self.logger.info("Interactive peer ready")

    def _print_known_peers(self):
        self.logger.info("Known peers: %s", list(self.known_peers))

    def on_release(self, key):
        """
        Method to handle input from keyboard.
        This method is not meant to be called directly.
        """

        if key.char in "sS":
            self.die()
            return False  # stops the listener
        if key.char in "lL":
            self._print_known_peers()
        return True

    def start(self):
        super().start()
        # setting up keyboard "shortcuts"
        with Listener(
            # on_press=InteractivePeer.on_press,
            on_release=self.on_release
        ) as listener:
            listener.join()
