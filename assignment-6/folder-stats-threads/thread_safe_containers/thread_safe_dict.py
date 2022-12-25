from collections import UserDict

from .thread_safe_container import ThreadSafeContainer


class ThreadSafeDict(UserDict, ThreadSafeContainer):

    def __init__(self, mapping=None, /, **kwargs):
        UserDict.__init__(self, mapping, **kwargs)
        ThreadSafeContainer.__init__(self)

    def __getitem__(self, item):
        return self.do_safe(super().__getitem__, item)

    def __setitem__(self, key, value):
        self.do_safe(super().__setitem__, key, value)

    def __delitem__(self, key):
        self.do_safe(super().__delitem__, key)
