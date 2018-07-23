# -*- coding: utf-8 -*-

from __future__ import absolute_import

from sqlpuzzle.exceptions import InvalidQueryException
from sqlpuzzle._common import SqlReference
from .values import Values

__all__ = ('OnConflictDoUpdate',)


class OnConflictDoUpdate(Values):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self._on_conflict = ''

    @property
    def _keyword_of_parts(self):
        return 'ON CONFLICT ({}) DO UPDATE'.format(self._on_conflict)

    def set(self, *args, **kwds):
        if args and isinstance(args[0], str):
            self._on_conflict = SqlReference(args[0])
            args = args[1:]
        else:
            raise InvalidQueryException('ON CONFLICT (column_name) DO UPDATE needs reference to column as first argument')
        super().set(*args, **kwds)
