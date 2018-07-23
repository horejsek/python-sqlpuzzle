# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six

from sqlpuzzle._queryparts import Columns, TablesForSelect, Where, GroupBy, Having, OrderBy, Limit, IntoOutfile
from .query import Query
from .union import Union, UNION, UNION_ALL
from .selectoptions import SelectOptions, SelectForUpdate

__all__ = ('Select',)


class Select(Query):
    """
    Examples:

    .. code-block:: python

        >>> sql = sqlpuzzle.select('id', 'name')
        >>> sql.from_('user')
        >>> sql.join('address').on('address.user_id', 'user.id')
        >>> sql.where({'user.name': sqlpuzzle.relations.LIKE('%Al%'), 'address.city': 'Prague'})
        >>> sql.group_by('user.id')
        >>> sql.order_by('user.name', ('user.sallary', 'desc'))
        >>> sql.limit(20)
        <Select:
            SELECT "id", "name"
                FROM "user" JOIN "address" ON "address"."user_id" = "user"."id"
                WHERE "address"."city" = 'Prague' AND "user"."name" LIKE '%Al%'
                GROUP BY "user"."id"
                ORDER BY "user"."name", "user"."sallary" DESC
                LIMIT 20
        >

        >>> sqlpuzzle.select('name').from_(sql).where(
        <Select: SELECT "name" FROM (...)>
    """

    _queryparts = {
        'select_options': SelectOptions,
        'columns': Columns,
        'tables': TablesForSelect,
        'where': Where,
        'group_by': GroupBy,
        'having': Having,
        'order_by': OrderBy,
        'limit': Limit,
        'into_outfile': IntoOutfile,
        'select_for_update': SelectForUpdate,
    }
    _query_template = six.u(
        'SELECT%(select_options)s%(columns)s%(tables)s'
        '%(where)s%(group_by)s%(having)s'
        '%(order_by)s%(limit)s%(into_outfile)s%(select_for_update)s'
    )

    def __init__(self, *args, **kwds):
        super(Select, self).__init__()
        self.columns(*args, **kwds)

    #  It's here just for shortcut, so you can call just `sql.has('distinct')`
    #+ instead of `sql.has('select_options', 'distinct')` (programmer does not
    #+ have to know about internal implementation).
    def has(self, querypart_name, value=None):
        """
        Returns ``True`` if ``querypart_name`` with ``value`` is set. For example
        you can check if you already used condition by ``sql.has('where')``.

        If you want to check for more information, for example if that condition
        also contain ID, you can do this by ``sql.has('where', 'id')``.
        """
        if super(Select, self).has(querypart_name, value):
            return True
        if not value:
            return super(Select, self).has('select_options', querypart_name)
        return False

    def __and__(self, other):
        """
        Returns :py:class:`sqlpuzzle._queries.union.Union` instance, ``UNION ALL``.

        .. code-block:: python

            >>> sqlpuzzle.select('t') & sqlpuzzle.select('u')
            <Union: SELECT "t" UNION ALL SELECT "u">
        """
        return Union(self, other, UNION_ALL)

    def __or__(self, other):
        """
        Returns :py:class:`sqlpuzzle._queries.union.Union` instance, ``UNION``.

        .. code-block:: python

            >>> sqlpuzzle.select('t') | sqlpuzzle.select('u')
            <Union: SELECT "t" UNION SELECT "u">
        """
        return Union(self, other, UNION)

    def columns(self, *args, **kwds):
        self._columns.columns(*args, **kwds)
        return self

    def from_(self, *args, **kwds):
        self._tables.set(*args, **kwds)
        return self

    def from_table(self, table, alias=None):
        self._tables.set((table, alias))
        return self

    from_tables = from_

    def join(self, table):
        self._tables.join(table)
        return self

    def inner_join(self, table):
        self._tables.inner_join(table)
        return self

    def left_join(self, table):
        self._tables.left_join(table)
        return self

    def right_join(self, table):
        self._tables.right_join(table)
        return self

    def full_join(self, table):
        """
        .. versionadded:: 1.7.0
        """
        self._tables.full_join(table)
        return self

    def on(self, *args, **kwds):
        self._tables.on(*args, **kwds)
        return self

    def where(self, *args, **kwds):
        self._where.where(*args, **kwds)
        return self

    def having(self, *args, **kwds):
        self._having.where(*args, **kwds)
        return self

    def group_by(self, *args, **kwds):
        """
        Default ordering is ``ASC``.

        ``group_by`` accept ``dict`` as you would expect, but note that ``dict``
        does not have same order. Same for named arguments.

        .. code-block:: python

            >>> sqlpuzzle.select('c').from_('t').group_by('a', ('b', 'desc'))
            <Select: SELECT "c" FROM "t" GROUP BY "a", "b" DESC>
        """
        self._group_by.group_by(*args, **kwds)
        return self

    def order_by(self, *args, **kwds):
        """
        Default ordering is ``ASC``.

        ``order_by`` accept ``dict`` as you would expect, but note that ``dict``
        does not have same order.

        .. code-block:: python

            >>> sqlpuzzle.select('c').from_('t').order_by('a', ('b', 'desc'))
            <Select: SELECT "c" FROM "t" ORDER BY "a", "b" DESC>
        """
        self._order_by.order_by(*args, **kwds)
        return self

    def limit(self, limit, offset=None):
        self._limit.limit(limit, offset)
        return self

    def offset(self, offset):
        self._limit.offset(offset)
        return self

    def into_outfile(self, into_outfile):
        self._into_outfile.into_outfile(into_outfile)
        return self

    def fields_terminated_by(self, fields_terminated_by):
        self._into_outfile.fields_terminated_by(fields_terminated_by)
        return self

    def lines_terminated_by(self, lines_terminated_by):
        self._into_outfile.lines_terminated_by(lines_terminated_by)
        return self

    def optionally_enclosed_by(self, optionally_enclosed_by):
        self._into_outfile.optionally_enclosed_by(optionally_enclosed_by)
        return self

    # SELECT OPTIONS

    def sql_cache(self, allow=True):
        self._select_options.sql_cache(allow)
        return self

    def sql_no_cache(self, allow=True):
        self._select_options.sql_no_cache(allow)
        return self

    def all(self, allow=True):
        self._select_options.all(allow)
        return self

    def distinct(self, allow=True):
        self._select_options.distinct(allow)
        return self

    def distinctrow(self, allow=True):
        self._select_options.distinctrow(allow)
        return self

    def sql_small_result(self, allow=True):
        self._select_options.sql_small_result(allow)
        return self

    def sql_big_result(self, allow=True):
        self._select_options.sql_big_result(allow)
        return self

    def sql_buffer_result(self, allow=True):
        self._select_options.sql_buffer_result(allow)
        return self

    def sql_calc_found_rows(self, allow=True):
        self._select_options.sql_calc_found_rows(allow)
        return self

    def straight_join(self, allow=True):
        self._select_options.straight_join(allow)
        return self

    def high_priority(self, allow=True):
        self._select_options.high_priority(allow)
        return self

    def for_update(self, allow=True):
        self._select_for_update.for_update(allow)
        return self
