# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six

from sqlpuzzle._queries.options import Options
from sqlpuzzle._queryparts import Tables, MultipleValues, OnDuplicateKeyUpdate
from .query import Query

__all__ = ('Insert',)


class InsertOptions(Options):
    _definition_of_options = {
        'ignore': {
            'off': '',
            'on': 'IGNORE',
        },
    }

    def ignore(self, allow=True):
        self._options['ignore'] = 'on' if allow else 'off'


class Insert(Query):
    """
    Example:

    .. code-block:: python

        >>> sql = sqlpuzzle.insert_into('table')
        >>> sql.values(name='Alan', salary=12345.67)
        >>> sql.values(name='Bob', age=42)
        <Insert: INSERT INTO "table" ("age", "name", "salary") VALUES (NULL, 'Alan', 12345.67000), (42, 'Bob', NULL)>
    """

    _queryparts = {
        'insert_options': InsertOptions,
        'tables': Tables,
        'values': MultipleValues,
        'on_duplicate_key_update': OnDuplicateKeyUpdate,
    }
    _query_template = six.u('INSERT%(insert_options)s INTO%(tables)s%(values)s%(on_duplicate_key_update)s')

    def into(self, table):
        self._tables.set(table)
        return self

    def values(self, *args, **kwds):
        self._values.add(*args, **kwds)
        return self

    def on_duplicate_key_update(self, *args, **kwds):
        self._on_duplicate_key_update.set(*args, **kwds)
        return self

    # INSERT OPTIONS

    def ignore(self, allow=True):
        self._insert_options.ignore(allow)
        return self
