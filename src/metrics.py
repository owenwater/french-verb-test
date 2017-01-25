import time
import sys

is_metrics = False


def runtime(func):
    def wrapper(*args, **kwargs):
        beg_ts = time.time()
        retval = func(*args, **kwargs)
        end_ts = time.time()
        if is_metrics:
            sys.stderr.write("elapsed time of \"%s\": %f\n" % (func.__name__, end_ts - beg_ts))
        return retval

    return wrapper
