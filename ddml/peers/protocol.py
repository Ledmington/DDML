# pylint: disable=missing-module-docstring
# pylint: disable=too-few-public-methods
class Protocol:
    """
    Container of all possible messages of the protocol used by the DDML peers.
    """

    NEW_MSG = "new"
    """
    The message sent when a peer comes alive.
    """

    HELLO_MSG = "hello"
    """
    This message is used to control if some other peer is still alive.
    """

    ALIVE_MSG = "alive"
    """
    This message is sent as response to HELLO_MSG to inform that the local peer is alive.
    """

    LEAVE_MSG = "bye"
    """
    The message sent when a peer dies gracefully.
    """
