import logging
from contextlib import ContextDecorator
from typing import Callable

logger = logging.getLogger(f'logger_conf.{__name__}')


class HandleErrorContext(ContextDecorator):

    def __init__(self,
                 exc_callback: Callable,
                 re_raise: bool = True,
                 log_traceback: bool = True,
                 exc_type: Exception or tuple[Exception, ...] = Exception):
        self._re_raise = re_raise
        self._log_traceback = log_traceback
        self._exc_callback = exc_callback

        if not isinstance(exc_type, tuple):
            self._exc_type = (exc_type,)
        else:
            self._exc_type = exc_type

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        is_handle_exception = any((issubclass(exc_type, exc_) for exc_ in self._exc_type))

        if is_handle_exception:
            if self._re_raise:
                raise exc_val
            else:
                self._exc_callback()
            if self._log_traceback:
                logger.exception(exc_tb)

        return self
