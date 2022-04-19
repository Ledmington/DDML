import pytest
import time
from ddml.utils.worker import Worker


def fake_task():
    time.sleep(1e-3)


def longn_task():
    time.sleep(1)


def test_worker_initially_dead():
    w = Worker(fake_task)
    assert w.is_shutdown() is False
    assert w.is_alive() is False


def test_task_must_be_lambda():
    for x in [None, 0, 1.5, True, (), [], {}, set()]:
        with pytest.raises(TypeError):
            w = Worker(x)


def test_when_started_is_alive():
    w = Worker(fake_task)
    w.start()
    assert w.is_shutdown() is False
    assert w.is_alive() is True
    w.die()
    w.join()


def test_cant_start_twice():
    w = Worker(fake_task)
    w.start()
    with pytest.raises(RuntimeError):
        w.start()
    w.die()
    w.join()


def test_is_shutdown_after_die():
    w = Worker(fake_task)
    w.start()
    w.die()
    assert w.is_shutdown() is True
    w.join()


def test_is_dead_after_join():
    w = Worker(fake_task)
    w.start()
    w.die()
    w.join()
    assert w.is_shutdown() is True
    assert w.is_alive() is False


def test_can_die_twice():
    w = Worker(fake_task)
    w.start()
    w.die()
    w.die()
    w.join()


def test_can_join_twice():
    w = Worker(fake_task)
    w.start()
    w.die()
    w.join()
    w.join()


def test_id_is_incremented():
    first_id = Worker.id
    w1 = Worker(fake_task)
    assert Worker.id == first_id + 1
    w2 = Worker(fake_task)
    assert Worker.id == first_id + 2
