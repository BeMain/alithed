import functools
import time


# Decorator for timing functions
def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(f"Executing {func.__name__} took {time.time()-start}")
        return res
    
    return wrapper 