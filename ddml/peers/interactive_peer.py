import sys
import logging

from ddml.peers.peer import Peer
from ddml.utils.colors import ColoredFormatter

def erase_one_line_before_logging(msg):
    print("\033[1A\033[K")
    print(msg)


class InteractivePeer(Peer):
    def __init__(self):
        Peer.__init__(self)
        self._setup_logger()

    def _setup_logger(self):
        # create logs directory
        # if not os.path.exists("logs"):
        #    os.mkdir("logs")

        logger = logging.getLogger("ddml-peer")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(asctime)s][%(levelname)s]: %(message)s", "%m-%d-%Y %H:%M:%S"
        )

        logger.log = erase_one_line_before_logging

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(ColoredFormatter())
        logger.addHandler(stdout_handler)

        # file_handler = logging.FileHandler("logs/ddml-peer.log")
        # file_handler.setLevel(logging.DEBUG)
        # file_handler.setFormatter(formatter)
        # logger.addHandler(file_handler)
