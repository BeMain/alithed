import functools
import time

CLEAR_WORLD_ON_STARTUP = False
ENABLE_LOGGING = True

def log(data):
    if ENABLE_LOGGING:
        print(data)


# Decorator for timing functions
def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        log(f"Executing {func.__name__} took {time.time()-start}")
        return res
    
    return wrapper 