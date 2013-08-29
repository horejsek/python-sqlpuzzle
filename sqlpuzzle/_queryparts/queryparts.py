# -*- coding: utf-8 -*-

import six

from functools import wraps

from sqlpuzzle._common import Object, force_text, is_sql_instance
from sqlpuzzle.exceptions import SqlPuzzleException

__all__ = ('QueryPart', 'QueryParts', 'append_custom_sql_decorator')


def append_custom_sql_decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwds):
        if not kwds and len(args) == 1 and is_sql_instance(args[0]):
            self.append_part(args[0])
            return self
        else:
            return func(self, *args, **kwds)
    return wrapper


class QueryPart(Object):
    def is_set(self):
        return True


class QueryParts(Object):
    _separator_of_parts = ', '
    _keyword_of_parts = ''
    _default_query_string = ''

    def __init__(self):
        super(QueryParts, self).__init__()
        self._parts = ListOfQueryParts(self._separator_of_parts)

    def __unicode__(self):
        if not self._parts:
            return six.text_type(self._default_query_string)
        if self._keyword_of_parts:
            return six.u('%s %s') % (self._keyword_of_parts, self._parts)
        return six.text_type(self._parts)

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

    def is_set(self):
        return bool(self._parts != [] or self._default_query_string)

    def append_unique_part(self, query_part):
        if query_part not in self:
            self.append_part(query_part)

    def append_part(self, query_part):
        self._parts.append(query_part)


class ListOfQueryParts(Object, list):
    def __init__(self, separator=''):
        super(ListOfQueryParts, self).__init__()
        self._separator = separator

    def append(self, query_part):
        if not is_sql_instance(query_part):
            raise SqlPuzzleException('Appended item must be instance of QueryPart, not %s.' % type(query_part))
        super(ListOfQueryParts, self).append(query_part)

    def __unicode__(self):
        return self._separator.join(force_text(f) for f in self)
