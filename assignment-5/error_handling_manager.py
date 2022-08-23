import contextlib
import logging
import sys

handler = logging.StreamHandler(stream=sys.stdout)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


@contextlib.contextmanager
def handle_error_context(re_raise: bool = True,
                         log_traceback: bool = True,
                         exc_type: Exception or tuple[Exception, ...] = Exception,):
    try:
        yield
    except exc_type as err:
        if re_raise:
            raise err
        if log_traceback:
            logger.exception(str(err))


if __name__ == '__main__':
    with handle_error_context(re_raise=False, log_traceback=True, exc_type=ValueError):
        raise ValueError()
