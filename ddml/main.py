# pylint: disable=missing-module-docstring
import sys
import os
import argparse
import termios

import ddml
from ddml.peers.peer import Peer


def _print_version():
    print("ddml-peer v" + ddml.__version__)


def _main(parser, arguments):
    if hasattr(arguments, "help"):
        _print_version()
        parser.print_help()
        sys.exit(0)
    elif hasattr(arguments, "version"):
        _print_version()
        sys.exit(0)

    _print_version()

    port = Peer.PORT
    if hasattr(arguments, "port"):
        port = arguments.port

    broadcast = True
    if hasattr(arguments, "no-broadcast"):
        broadcast = False

    peers = []
    if hasattr(arguments, "peers"):
        # file
        if os.path.exists(arguments.peers):
            with open(arguments.peers, "r", encoding=sys.getdefaultencoding()) as file:
                peers = list(file)
        # list of values
        else:
            peers = arguments.peers.split(",")

    if hasattr(arguments, "interactive"):
        # pylint: disable=import-outside-toplevel
        from ddml.peers.interactive_peer import InteractivePeer

        msg = "Starting an interactive peer"
        print(msg + "\n" + "=" * len(msg) + "\n")
        peer = InteractivePeer(port=port, broadcast=broadcast, peers=peers)
    else:
        msg = "Starting a non-interactive peer"
        print(msg + "\n" + ("=" * len(msg)))
        peer = Peer(port=port, broadcast=broadcast, peers=peers)

    peer.start()
    peer.join()


def _setup_parser():
    parser = argparse.ArgumentParser(
        description="A peer designed to train machine learning models in a "
        + "decentralized and distributed manner.",
        allow_abbrev=False,
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-h",
        "--help",
        default=argparse.SUPPRESS,
        action="store_true",
        help="Print this help message and exit",
    )
    parser.add_argument(
        "-v",
        "--version",
        default=argparse.SUPPRESS,
        action="store_true",
        help="Print version number and exit",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        default=argparse.SUPPRESS,
        action="store_true",
        help="Enable interactive mode",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=Peer.PORT,
        type=int,
        help="The port number to be used by the peer",
    )
    parser.add_argument(
        "--no-broadcast",
        default=argparse.SUPPRESS,
        action="store_true",
        help="Tells the peer to broadcast first and last messages on the LAN",
    )
    parser.add_argument(
        "--peers",
        default=argparse.SUPPRESS,
        type=str,
        help="List of peers known in advance. Can be a sequence of comma separated "
        + "IP addresses or a filename containing newline separated IP addresses.",
    )

    return parser


if __name__ == "__main__":
    arg_parser = _setup_parser()

    args = arg_parser.parse_args()

    _main(arg_parser, args)
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)
