import logging
from pynput.keyboard import Key, Listener

from ddml.peers.peer import Peer
from ddml.utils.colors import ColoredFormatter


class InteractivePeer(Peer):
    class CustomFormatter(ColoredFormatter):
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

    def __init__(self):
        Peer.__init__(self, log_fmt=self.CustomFormatter())
        self.logger.info("Interactive peer ready")

    def on_press(key):
        print("{0} pressed".format(key))

    def on_release(key):
        print("{0} release".format(key))
        if key == Key.esc:
            # Stop listener
            return False

    def start(self):
        super().start()
        # setting up keyboard "shortcuts"
        with Listener(
            on_press=InteractivePeer.on_press, on_release=InteractivePeer.on_release
        ) as listener:
            listener.join()
