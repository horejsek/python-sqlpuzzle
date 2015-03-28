# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six

from sqlpuzzle.exceptions import ConfirmUpdateAllException
from sqlpuzzle._queries.options import Options
from sqlpuzzle._queryparts import Tables, Values, Where
from .query import Query

__all__ = ('Update',)


class UpdateOptions(Options):
    _definition_of_options = {
        'ignore': {
            'off': '',
            'on': 'IGNORE',
        },
    }

    def ignore(self, allow=True):
        self._options['ignore'] = 'on' if allow else 'off'


class Update(Query):
    _queryparts = {
        'update_options': UpdateOptions,
        'tables': Tables,
        'values': Values,
        'where': Where,
    }
    _query_template = six.u('UPDATE%(update_options)s%(tables)s SET%(values)s%(where)s')

    def __init__(self, table=None):
        super(Update, self).__init__()
        self._allow_update_all = False
        self.table(table)

    def __unicode__(self):
        if not self._where.is_set and not self._allow_update_all:
            raise ConfirmUpdateAllException()
        return super(Update, self).__unicode__()

    def allow_update_all(self):
        """Allow query without WHERE condition."""
        self._allow_update_all = True
        return self

    def forbid_update_all(self):
        """Forbid query without WHERE condition."""
        self._allow_update_all = False
        return self

    def table(self, table):
        self._tables.set(table)
        return self

    def set(self, *args, **kwds):
        """
        set(name='Michael', country=None)
        set({'age': 20, 'enabled': True})
        set('last_modify', datetime.datetime(2011, 6, 15, 22, 11, 00))
        set([('id', 20), ('name', 'Harry')])
        """
        self._values.set(*args, **kwds)
        return self

    def where(self, *args, **kwds):
        """
        where(name='Michael', country=None)
        where({'age': 20, 'enabled': True})
        where('last_modify', datetime.datetime(2011, 6, 15, 22, 11, 00))
        where('id', range(10, 20, 2))
        where([('id', 20), ('name', sqlpuzzle.relation.LIKE('%ch%'))])
        """
        self._where.where(*args, **kwds)
        return self

    def join(self, table):
        """
        join('table')
        join(('table', 'asTable'))
        join({'table': 'asTable'})
        """
        self._tables.join(table)
        return self

    def inner_join(self, table):
        """
        inner_join('table')
        inner_join(('table', 'asTable'))
        inner_join({'table': 'asTable'})
        """
        self._tables.inner_join(table)
        return self

    def left_join(self, table):
        """
        left_join('table')
        left_join(('table', 'asTable'))
        left_join({'table': 'asTable'})
        """
        self._tables.left_join(table)
        return self

    def right_join(self, table):
        """
        right_join('table')
        right_join(('table', 'asTable'))
        right_join({'table': 'asTable'})
        """
        self._tables.right_join(table)
        return self

    def on(self, *args, **kwds):
        """
        on(id='another_id')
        on({'table1.id': 'table2.another_id'})
        on([('table1.id', 'table2.another_id')])
        """
        self._tables.on(*args, **kwds)
        return self

    # UPDATE OPTIONS

    def ignore(self, allow=True):
        self._update_options.ignore(allow)
        return self

    # Backward compatibility.

    allowUpdateAll = allow_update_all
    forbidUpdateAll = forbid_update_all
