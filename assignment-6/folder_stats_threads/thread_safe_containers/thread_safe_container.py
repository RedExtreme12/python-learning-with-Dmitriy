from threading import Lock
from typing import Callable, Any


class ThreadSafeContainer:
    """
    A class that is the basis for safe container implementations.
    """

    def __init__(self):
        self._lock = Lock()

    def do_safe(self, method: Callable, *args, **kwargs) -> Any:
        """
        A wrapper method that executes the passed method safely.
        param method: wrapped method of container
        param args: positional arguments of wrapped method.
        param kwargs: named arguments of wrapped method.
        :return: Any
        """
        with self._lock:
            return method(*args, **kwargs)
