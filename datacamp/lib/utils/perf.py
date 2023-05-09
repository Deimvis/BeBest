import cProfile
import functools
import logging


def perf(output_file_path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            profile = cProfile.Profile()
            profile.enable()
            logging.debug('Profiling enabled')
            result = func(*args, **kwargs)
            profile.disable()
            logging.debug('Profiling disabled')
            profile.dump_stats(output_file_path)
            return result
        return wrapper
    return decorator
