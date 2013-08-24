# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six

from sqlpuzzle._common import check_type_decorator
from .queryparts import QueryPart

__all__ = ('Limit',)


class Limit(QueryPart):
    def __init__(self, limit=None, offset=None):
        super(Limit, self).__init__()
        self._limit = limit
        self._offset = offset

    def __unicode__(self):
        limit = six.u('LIMIT %s') % self._limit
        if self._offset is not None:
            limit = six.u('%s OFFSET %s') % (limit, self._offset)
        return limit

    def __eq__(self, other):
        return (
            type(self) == type(other) and
            self._limit == other._limit and
            self._offset == other._offset
        )

    def is_set(self):
        return self._limit is not None

    @check_type_decorator(six.integer_types + (type(None),))
    def limit(self, limit, offset=None):
        if limit is None:
            self._limit = None
            self._offset = None
        else:
            self._limit = int(limit)
            if offset is not None:
                self.offset(offset)
        return self

    @check_type_decorator(six.integer_types + (type(None),))
    def offset(self, offset):
        self._offset = int(offset) if offset else None
        return self
