import sys

from ddml.peers.peer import Peer
from ddml.utils.colors import colored

if __name__ == "__main__":
    interactive_mode = False
    for arg in sys.argv[1:]:
        if arg in ["-i", "--interactive"]:
            interactive_mode = True
        else:
            print(colored("ERROR", "red"), f': unknown argument "{arg}"')

    if interactive_mode is True:
        from ddml.peers.interactive_peer import InteractivePeer

        print("Starting an interactive peer")
        p = InteractivePeer()
        p.start()
        p.join()
    else:
        print("Starting a non-interactive peer")
        p = Peer()
        p.start()
        p.join()
