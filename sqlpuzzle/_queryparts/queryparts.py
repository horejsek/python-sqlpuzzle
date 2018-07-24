from functools import wraps
import re

from sqlpuzzle._common import Object, force_text, is_sql_instance
from sqlpuzzle.exceptions import SqlPuzzleException

__all__ = ('QueryPart', 'QueryParts', 'append_custom_sql_decorator', 'has')


def append_custom_sql_decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwds):
        if not kwds and len(args) == 1 and is_sql_instance(args[0]):
            self.append_part(args[0])
            return self
        return func(self, *args, **kwds)
    return wrapper


def has(part, value):
    value = force_text(value)
    #  If I look for example for "distinct", I don't want to say "hey, there is
    #+ distinct!", if there is actually "distinctrow".
    res = re.search(r'([^\w]|^){}([^\w]|$)'.format(value), str(part))
    return bool(res)


class QueryPart(Object):
    @property
    def is_set(self):
        return True

    def has(self, value):
        return has(self, value)


class QueryParts(Object):
    _separator_of_parts = ', '
    _keyword_of_parts = ''
    _default_query_string = ''

    def __init__(self):
        super().__init__()
        self._parts = ListOfQueryParts(self._separator_of_parts)

    def __str__(self):
        if not self._parts:
            return str(self._default_query_string)
        if self._keyword_of_parts:
            return '%s %s' % (self._keyword_of_parts, self._parts)
        return str(self._parts)

    def __contains__(self, other_part):
        for part in self._parts:
            if part == other_part:
                return True
        return False

    def __eq__(self, other):
        if not isinstance(other, QueryParts) or len(self._parts) != len(other._parts):
            return False
        return all(sp == op for sp, op in zip(self._parts, other._parts))

    @property
    def count_of_parts(self):
        return len(self._parts)

    @property
    def is_set(self):
        return bool(self._parts != [] or self._default_query_string)

    def has(self, value):
        return has(self, value)

    def append_unique_part(self, query_part):
        if query_part not in self:
            self.append_part(query_part)

    def append_part(self, query_part):
        self._parts.append(query_part)


class ListOfQueryParts(Object, list):
    def __init__(self, separator=''):
        super().__init__()
        self._separator = separator

    def append(self, query_part):
        if not is_sql_instance(query_part):
            raise SqlPuzzleException('Appended item must be instance of QueryPart, not %s.' % type(query_part))
        super().append(query_part)

    def __str__(self):
        return self._separator.join(force_text(f) for f in self)
