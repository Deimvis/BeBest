import functools
import time


class MaxRetriesReachedError(Exception):
    pass


def try_while(*, while_=lambda: False, sleep_time_s=60, max_retries=120, max_retries_error_msg=''):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retry_index = 0
            while while_():
                if retry_index >= max_retries:
                    raise MaxRetriesReachedError('Max retries reached: {}'.format(max_retries_error_msg))
                if retry_index > 0:
                    time.sleep(sleep_time_s)
                func(*args, **kwargs)
                retry_index += 1
        return wrapper
    return decorator


def call_delay(*, seconds=0, minutes=0, hours=0):
    delay_s = seconds + minutes * 60 + hours * 3600
    call_delay.last_call = -1

    def decorator(func):

        def wait_delay():
            now = int(time.time())
            time.sleep(max(call_delay.last_call + delay_s - now, 0))

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait_delay()
            call_delay.last_call = int(time.time())
            return func(*args, **kwargs)

        return wrapper
    return decorator


def max_calls_per_second(count):
    return call_delay(seconds = 1.0 / count)
