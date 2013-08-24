# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six

from sqlpuzzle._queryparts import Tables, MultipleValues, OnDuplicateKeyUpdate
from .query import Query

__all__ = ('Insert',)


class Insert(Query):
    _queryparts = {
        'tables': Tables,
        'values': MultipleValues,
        'on_duplicate_key_update': OnDuplicateKeyUpdate,
    }
    _query_template = six.u('INSERT INTO%(tables)s%(values)s%(on_duplicate_key_update)s')

    def into(self, table):
        """
        into('user', 'country', ...)
        into(('user', 'asUser'), ('user', 'asParent'))
        into({'user': 'asUser', 'user', 'asParent'})
        """
        self._tables.set(table)
        return self

    def values(self, *args, **kwds):
        """
        values(name='Michael', country=None)
        values({'age': 20, 'enabled': True})
        values('last_modify', datetime.datetime(2011, 6, 15, 22, 11, 00))
        values([('id', 20), ('name', 'Harry')])
        """
        self._values.add(*args, **kwds)
        return self

    def on_duplicate_key_update(self, *args, **kwds):
        """
        on_duplicate_key_update(name='Michael', country=None)
        on_duplicate_key_update({'age': 20, 'enabled': True})
        on_duplicate_key_update('last_modify', datetime.datetime(2011, 6, 15, 22, 11, 00))
        on_duplicate_key_update([('id', 20), ('name', 'Harry')])
        """
        self._on_duplicate_key_update.set(*args, **kwds)
        return self
