import logging

# ANSI colors
grey = "\x1b[38;20m"
blue = "\x1b[34;40m"
yellow = "\x1b[33;20m"
red = "\x1b[31;20m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"


def colored(msg: str, color: str):
    colors = {"grey": grey, "blue": blue, "yellow": yellow, "red": red, "bold_red": red}
    if color not in colors:
        raise ValueError(f'Invalid color "{color}"')
    return colors[color] + msg + reset


class ColoredFormatter(logging.Formatter):

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
        return formatter.format(record)
