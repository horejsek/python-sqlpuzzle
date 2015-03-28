# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six

from sqlpuzzle.exceptions import ConfirmDeleteAllException
from sqlpuzzle._queries.options import Options
from sqlpuzzle._queryparts import Tables, Where
from .query import Query

__all__ = ('Delete',)


class DeleteOptions(Options):
    _definition_of_options = {
        'ignore': {
            'off': '',
            'on': 'IGNORE',
        },
    }

    def ignore(self, allow=True):
        self._options['ignore'] = 'on' if allow else 'off'


class Delete(Query):
    _queryparts = {
        'delete_options': DeleteOptions,
        'tables': Tables,
        'references': Tables,
        'where': Where,
    }
    _query_template = six.u('DELETE%(delete_options)s%(tables)s FROM%(references)s%(where)s')

    def __init__(self, *tables):
        super(Delete, self).__init__()
        self._allow_delete_all = False
        self._tables.set(*tables)

    def __unicode__(self):
        if not self._where.is_set and not self._allow_delete_all:
            raise ConfirmDeleteAllException()
        return super(Delete, self).__unicode__()

    def allow_delete_all(self):
        """Allow query without WHERE condition."""
        self._allow_delete_all = True
        return self

    def forbid_delete_all(self):
        """Forbid query without WHERE condition."""
        self._allow_delete_all = False
        return self

    def delete(self, *tables):
        self._tables.set(*tables)
        return self

    def from_(self, *args, **kwds):
        """
        from_('user', 'country', ...)
        from_(('user', 'asUser'), ('user', 'asParent'))
        from_({'user': 'asUser', 'user', 'asParent'})
        """
        self._references.set(*args, **kwds)
        return self

    def from_table(self, table, alias=None):
        """
        from_table('user')
        from_table('user', alias='asUser')
        """
        self._references.set((table, alias))
        return self

    def from_tables(self, *args, **kwds):
        """
        from_tables('user', 'country', ...)
        from_tables(('user', 'asUser'), ('user', 'asParent'))
        from_tables({'user': 'asUser', 'user', 'asParent'})
        """
        self.from_(*args, **kwds)
        return self

    def join(self, table):
        """
        join('table')
        join(('table', 'asTable'))
        join({'table': 'asTable'})
        """
        self._references.join(table)
        return self

    def inner_join(self, table):
        """
        inner_join('table')
        inner_join(('table', 'asTable'))
        inner_join({'table': 'asTable'})
        """
        self._references.inner_join(table)
        return self

    def left_join(self, table):
        """
        left_join('table')
        left_join(('table', 'asTable'))
        left_join({'table': 'asTable'})
        """
        self._references.left_join(table)
        return self

    def right_join(self, table):
        """
        right_join('table')
        right_join(('table', 'asTable'))
        right_join({'table': 'asTable'})
        """
        self._references.right_join(table)
        return self

    def on(self, *args, **kwds):
        """
        on(id='another_id')
        on({'table1.id': 'table2.another_id'})
        on([('table1.id', 'table2.another_id')])
        """
        self._references.on(*args, **kwds)
        return self

    def where(self, *args, **kwds):
        """
        where(name='Michael', country=None)
        where({'age': 20, 'enabled': True})
        where('last_modify', datetime.datetime(2011, 6, 15, 22, 11, 00))
        where('id', range(10, 20, 2), sqlpuzzle.relations.IN)
        where([('id', 20), ('name', '%ch%', sqlpuzzle.relation.LIKE)])
        """
        self._where.where(*args, **kwds)
        return self

    # DELETE OPTIONS

    def ignore(self, allow=True):
        self._delete_options.ignore(allow)
        return self


    # Backward compatibility.

    allowDeleteAll = allow_delete_all
    forbidDeleteAll = forbid_delete_all
    fromTable = from_table
    fromTables = from_tables
    innerJoin = inner_join
    leftJoin = left_join
    rightJoin = right_join
