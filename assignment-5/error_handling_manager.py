import contextlib
import logging
import sys
import time

from functools import wraps
from itertools import count

handler = logging.StreamHandler(stream=sys.stdout)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


@contextlib.contextmanager
def handle_error_context(re_raise: bool = True,
                         log_traceback: bool = True,
                         exc_type: Exception or tuple[Exception, ...] = Exception,
                         attempt_number: int = 0,
                         tries: int = 1):
    try:
        yield
    except exc_type as err:
        if (attempt_number + 1) == tries:
            if re_raise:
                raise err
            if log_traceback:
                logger.exception(str(err))


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
            _delay = delay

            iterator = range(tries) if tries is not None else count(0)

            for attempt_number in iterator:
                logger.debug(f'The attempt {attempt_number} has begun!')
                with handle_error_context(re_raise, log_traceback, exc_type, attempt_number, tries):
                    return func(*args, **kwargs)

                time.sleep(_delay)
                _delay *= backoff

        return wrapper

    return inner


@handle_error(re_raise=False, delay=10)
def some_function():
    x = 1 / 0  # ZeroDivisionError


if __name__ == '__main__':
    some_function()
    print(1)
