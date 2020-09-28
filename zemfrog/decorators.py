from functools import wraps
from typing import Callable


def auto_status_code(func: Callable) -> Callable:
    """
    Decorator to generate HTTP status response code automatically
    according to the key ``status_code`` in json.

    :param func: Your view function.

    """

    @wraps(func)
    def wrapper(*args, **kwds):
        result = func(*args, **kwds)
        status_code = 200
        if isinstance(result, dict):
            status_code = result.get("status_code", 200)

        if not isinstance(result, (tuple, list)):
            result = result, status_code

        return result

    return wrapper
