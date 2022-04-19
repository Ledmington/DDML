from threading import Thread


class Worker(Thread):
    id = 0

    def __init__(self, task, name=None):
        if not callable(task):
            raise TypeError

        if name is None:
            name = "worker-" + str(Worker.id)
            Worker.id += 1

        self.task = task
        self.shutdown = False

        Thread.__init__(self, target=self._loop, name=name, daemon=False)

    def is_shutdown(self) -> bool:
        return self.shutdown

    def is_alive(self) -> bool:
        return Thread.is_alive(self)

    def start(self):
        Thread.start(self)

    def _loop(self):
        while self.shutdown is False:
            self.task()

    def die(self):
        self.shutdown = True

    def join(self):
        Thread.join(self)
