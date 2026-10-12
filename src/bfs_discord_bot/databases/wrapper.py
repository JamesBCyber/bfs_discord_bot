from functools import wraps


def save_method(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self._root.save()
        return result

    return wrapper
