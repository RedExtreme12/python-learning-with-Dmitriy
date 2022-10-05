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
        exc_type: Exception or tuple[Exception, ...] = Exception,
        tries: int | None = 1,
        delay: int | float = 0,
        backoff: int = 1
):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            exception = None
            _delay = delay

            iterator = range(tries) if tries is not None else count(0)

            for _ in iterator:
                try:
                    return func(*args, **kwargs)
                except exc_type as err:
                    print(exc_type)
                    if re_raise:
                        print(re_raise)
                        exception = err
                    if log_traceback:
                        logger.exception(str(err))
                except Exception as err:
                    exception = err

                time.sleep(_delay)
                _delay *= backoff

            if exception:
                raise exception

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


@handle_error(re_raise=False, exc_type=KeyError, delay=2)
def some_function():
    x = 1 / 0  # ZeroDivisionError


if __name__ == '__main__':
    some_function()
    print(1)

    # with HandleErrorContext(re_raise=False, log_traceback=True, exc_type=ValueError):
    #     raise ValueError()
