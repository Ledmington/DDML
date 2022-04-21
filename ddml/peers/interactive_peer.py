import sys
import logging
from pynput.keyboard import Key, Listener

from ddml.peers.peer import Peer
from ddml.utils.colors import colored


class InteractivePeer(Peer):
    class CustomFormatter(logging.Formatter):
        erase_one_line = "\033[1A\033[K"
        commands_bar = "[S]top | [L]ist | [T]rain"

        time = "[%(asctime)s]"
        level = "%(levelname)s"
        msg = "%(message)s"

        FORMATS = {
            logging.DEBUG: time + "[" + colored(level, "grey") + "]: " + msg,
            logging.INFO: time + "[" + colored(level, "blue") + "]: " + msg,
            logging.WARNING: time + "[" + colored(level, "yellow") + "]: " + msg,
            logging.ERROR: time + "[" + colored(level, "red") + "]: " + msg,
            logging.CRITICAL: colored(time + "[" + level + "]: " + msg, "bold_red"),
        }

        def format(self, record):
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            return (
                self.erase_one_line
                + formatter.format(record)
                + "\n"
                + self.commands_bar
            )

    def __init__(self):
        Peer.__init__(self)
        self._setup_logger()
        self.logger.info("Interactive peer ready")

    def on_press(key):
        print("{0} pressed".format(key))

    def on_release(key):
        print("{0} release".format(key))
        if key == Key.esc:
            # Stop listener
            return False

    def _setup_logger(self):
        # create logs directory
        # if not os.path.exists("logs"):
        #    os.mkdir("logs")

        self.logger = logging.getLogger("ddml-peer")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(asctime)s][%(levelname)s]: %(message)s", "%m-%d-%Y %H:%M:%S"
        )

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(self.CustomFormatter())
        self.logger.addHandler(stdout_handler)

        # file_handler = logging.FileHandler("logs/ddml-peer.log")
        # file_handler.setLevel(logging.DEBUG)
        # file_handler.setFormatter(formatter)
        # logger.addHandler(file_handler)

    def start(self):
        super().start()
        # setting up keyboard "shortcuts"
        with Listener(
            on_press=InteractivePeer.on_press, on_release=InteractivePeer.on_release
        ) as listener:
            listener.join()
