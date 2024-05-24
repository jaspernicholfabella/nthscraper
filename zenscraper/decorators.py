from zenscraper.logger import setup_logger
import functools
import time

logger = setup_logger()


def timer(func):
    """Decorator that print the runtime of a function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        logger.info(f"Finished {func.__name__!r} in {run_time:.6f} secs")
        return value

    return wrapper_timer


def retry(exception=Exception, tries: int = 1, init_wait: int = 60, factor: int = 2):
    """
    Decorator to retry a function

    :param exception: Exception(s) that triggers a retry, can be a tuple.
    :param tries: Total tries
    :param init_wait: Seconds to fire retry
    :param factor: Backoff Multiplier
    :return:
    """

    def retry_decorator(func):
        @functools.wraps(func)
        def retry_wrapper(*args, **kwargs):
            fmsg = f"args={args if args else ''}, kwargs = {kwargs}"
            for _try in range(tries):
                try:
                    logger.info(f"Trying({_try+1}): func={func.__name__}")
                    logger.debug(fmsg)
                    return func(*args, **kwargs)
                except Exception as e:
                    _delay = (factor**_try) * init_wait
                    if _try == tries - 1:
                        raise
                    logger.exception(e)
                    logger.info(
                        f"""Retrying on: func={func.__name__},
                        delay={_delay} seconds,
                        exception={repr(e)}"""
                    )
                    time.sleep(_delay)
            return retry_wrapper

        return retry_decorator
