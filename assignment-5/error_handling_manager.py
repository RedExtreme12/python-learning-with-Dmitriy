import contextlib
import time
import logging
import sys
from functools import wraps

from itertools import count

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
                    yield func(*args, **kwargs)
                except exc_type as err:
                    if re_raise:
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


@contextlib.contextmanager
def handle_error_context(re_raise: bool = True,
                         log_traceback: bool = True,
                         exc_type: Exception or tuple[Exception, ...] = Exception,):

    @handle_error(re_raise=re_raise, log_traceback=log_traceback, exc_type=exc_type)
    def wrapper():
        yield

    yield from wrapper()


if __name__ == '__main__':
    with handle_error_context(log_traceback=True, exc_type=ValueError):
        raise ValueError()
