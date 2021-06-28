import functools
import time

CLEAR_WORLD_ON_STARTUP = True
ENABLED_LOGGING_PRIORITY = 2    # 3: Unimportant information
                                # 2: Notes
                                # 1: Errors
                                # 0: Temporary logging 

def log(data, priority = 0):
    if priority <= ENABLED_LOGGING_PRIORITY:
        print(data)


def timeit(func):
    """Decorator for timing functions"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        log(f"Executing {func.__name__} took {time.time()-start}", priority=0)
        return res
    
    return wrapper 