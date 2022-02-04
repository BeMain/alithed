import functools

paused = False


# Decorator for marking which functions to pause
def pausable(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not paused:
            return func(*args, **kwargs)
        return None

    return wrapper
