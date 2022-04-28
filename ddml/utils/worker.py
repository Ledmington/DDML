from threading import Thread


class Worker(Thread):
    """
    TODO
    """

    id = 0

    def __init__(self, task, name=None):
        """
        TODO
        """
        
        if not callable(task):
            raise TypeError

        if name is None:
            name = "worker-" + str(Worker.id)
            Worker.id += 1

        self.task = task
        self.shutdown = False

        Thread.__init__(self, target=self._loop, name=name, daemon=False)

    def is_shutdown(self) -> bool:
        """
        TODO
        """
        
        return self.shutdown

    def is_alive(self) -> bool:
        """
        TODO
        """
        
        return Thread.is_alive(self)

    def start(self):
        """
        TODO
        """
        
        Thread.start(self)

    def _loop(self):
        while self.shutdown is False:
            self.task()

    def die(self):
        """
        Tells the worker to terminate.
        
        This is a non-blocking call. To wait for Worker's death, use join().
        """
        
        self.shutdown = True

    def join(self):
        """
        Waits for the Worker to terminate.
        """
        
        Thread.join(self)
