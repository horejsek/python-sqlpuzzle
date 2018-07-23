from functools import wraps

from sqlpuzzle.exceptions import InvalidArgumentException

__all__ = ('force_text', 'is_sql_instance', 'check_type_decorator')


def force_text(value):
    if is_sql_instance(value):
        return value.tosql()
    return str(value)


def is_sql_instance(value):
    return hasattr(value, 'tosql')


def check_type_decorator(allowed_types=()):
    def decorator(func):
        @wraps(func)
        def wrapper(self, value, *args, **kwds):
            if (
                    (not isinstance(value, allowed_types) or (isinstance(value, bool) and bool not in allowed_types))
                    and not hasattr(value, 'tosql')
            ):
                raise InvalidArgumentException('%s cannot be of type %s.' % (
                    func.__name__,
                    type(value),
                ))
            return func(self, value, *args, **kwds)
        return wrapper
    return decorator
