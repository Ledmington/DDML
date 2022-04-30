"""
Simple module containing just the Worker class.
"""

from threading import Thread


class Worker(Thread):
    """
    Utility class that represents a Thread that never terminate by itself.
    """

    id = 0

    def __init__(self, task, name=None):
        """
        Creates the Worker without starting it.

        Args:
            task: the task to be executed in each iteration of an infinite loop
            name: an optional string

        Raises:
            TypeError: if task is not a callable
        """

        if not callable(task):
            raise TypeError("task must be a callable")

        if name is None:
            name = "worker-" + str(Worker.id)
            Worker.id += 1

        self.task = task
        self.shutdown = False

        Thread.__init__(self, target=self._loop, name=name, daemon=False)

    def is_shutdown(self) -> bool:
        """
        Checks whether the Worker is shutdown or not.

        A shutdown Worker does not terminate istantly, it executes the task one
        last time.

        Returns:
            True if it if shutdown, False otherwise
        """

        return self.shutdown

    def is_alive(self) -> bool:
        return Thread.is_alive(self)

    def start(self):
        Thread.start(self)

    def _loop(self):
        while self.shutdown is False:
            self.task()

    def die(self):
        """
        Shuts down the Worker.

        This is a non-blocking call. To wait for Worker's termination, use join().
        """

        self.shutdown = True

    def join(self, timeout=None):
        Thread.join(self, timeout)
