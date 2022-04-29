import logging

# ANSI colors
GREY = "\x1b[38;20m"
BLUE = "\x1b[34;40m"
YELLOW = "\x1b[33;20m"
RED = "\x1b[31;20m"
BOLD_RED = "\x1b[31;1m"
RESET = "\x1b[0m"


def colored(msg: str, color: str):
    colors = {
        "grey": GREY,
        "blue": BLUE,
        "yellow": YELLOW,
        "red": RED,
        "bold_red": BOLD_RED,
    }
    if color not in colors:
        raise ValueError(f'Invalid color "{color}"')
    return colors[color] + msg + RESET


class ColoredFormatter(logging.Formatter):

    time = "[%(asctime)s]"
    level = "%(levelname)s"
    msg = "%(message)s"

    FORMATS = {
        logging.DEBUG: f'[{time}][{colored(level, "grey")}]: {msg}',
        logging.INFO: time + "[" + colored(level, "blue") + "]: " + msg,
        logging.WARNING: time + "[" + colored(level, "yellow") + "]: " + msg,
        logging.ERROR: time + "[" + colored(level, "red") + "]: " + msg,
        logging.CRITICAL: colored(time + "[" + level + "]: " + msg, "bold_red"),
    }

    def format(self, record):
        log_fmt = self.FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
