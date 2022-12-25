from typing import Any

from .thread_safe_container import ThreadSafeContainer


class ThreadSafeSet(set, ThreadSafeContainer):

    def __init__(self, *args):
        set.__init__(self, args)
        ThreadSafeContainer.__init__(self)

    def add(self, value: Any):
        self.do_safe(super().add, value)

    def clear(self):
        self.do_safe(super().clear)

    def remove(self, element: Any):
        self.do_safe(super().remove, element)

    def discard(self, element: Any):
        self.do_safe(super().discard, element)
