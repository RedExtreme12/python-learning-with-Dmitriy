import time
import logging
import sys
from functools import wraps

from itertools import count
from contextlib import contextmanager, ContextDecorator

handler = logging.StreamHandler(stream=sys.stdout)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def handle_error(
        re_raise: bool = True,
        log_traceback: bool = True,
        exc_type: Exception | tuple = Exception,
        tries: int | None = 1,
        delay: int | float = 0,
        backoff: int = 1
):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _delay = delay

            iterator = range(tries) if tries is not None else count(0)

            for attempt in iterator:
                logger.debug(f'The attempt {attempt} has begun')
                try:
                    return func(*args, **kwargs)
                except exc_type as err:
                    if (attempt + 1) == tries:
                        if re_raise:
                            raise err
                        if log_traceback:
                            logger.exception(str(err))

                time.sleep(_delay)
                _delay *= backoff

        return wrapper

    return inner


class HandleErrorContext(ContextDecorator):

    def __init__(self, re_raise: bool = True, log_traceback: bool = True, exc_type=Exception):
        self._re_raise = re_raise
        self._log_traceback = log_traceback
        self._exc_type = (exc_type,)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type in self._exc_type:
            if self._re_raise:
                raise exc_val
            if self._log_traceback:
                logger.exception(exc_tb)

        return self


@handle_error(re_raise=True, exc_type=(ValueError, ZeroDivisionError), delay=1, tries=3, log_traceback=False)
def some_function():
    x = 1 / 0


if __name__ == '__main__':
    some_function()
    print(1)
