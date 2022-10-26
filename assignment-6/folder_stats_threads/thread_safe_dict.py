from collections import UserDict
from threading import Lock


class ThreadSafeDict(UserDict):

    def __init__(self, mapping=None, /, **kwargs):
        self._lock = Lock()
        super().__init__(mapping, **kwargs)

    def __getitem__(self, item):
        with self._lock:
            return super().__getitem__(item)

    def __setitem__(self, key, value):
        with self._lock:
            super().__setitem__(key, value)

    def __delitem__(self, key):
        with self._lock:
            super().__delitem__(key)
