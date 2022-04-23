import sys
import argparse

from ddml.utils.colors import colored


def print_version():
    import ddml

    print("ddml-peer v" + ddml.__version__)


def set_interactive_mode(config: dict):
    config["interactive"] = True


def main(arguments):
    print_version()

    if arguments.interactive is True:
        from ddml.peers.interactive_peer import InteractivePeer

        msg = "Starting an interactive peer"
        print(msg + "\n" + "=" * len(msg) + "\n")
        p = InteractivePeer()
        p.start()
        p.join()
    else:
        from ddml.peers.peer import Peer

        msg = "Starting a non-interactive peer"
        print(msg + "\n" + ("=" * len(msg)))
        p = Peer()
        p.start()
        p.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A peer designed to train machine learning models in a decentralized and distributed manner.",
        allow_abbrev=False,
        add_help=False,
    )
    parser.add_argument(
        "-h",
        "--help",
        default=None,
        action="store_true",
        help="Print this help message and exit",
    )
    parser.add_argument(
        "-v",
        "--version",
        default=None,
        action="store_true",
        help="Print version number and exit",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        default=None,
        action="store_true",
        help="Enable interactive mode",
    )

    args = parser.parse_args()

    if args.help is not None:
        print_version()
        parser.print_help()
        sys.exit(0)
    elif args.version is not None:
        print_version()
        sys.exit(0)

    main(args)
