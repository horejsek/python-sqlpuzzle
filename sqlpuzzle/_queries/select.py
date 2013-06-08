# -*- coding: utf-8 -*-

import sqlpuzzle._queries.union

import sqlpuzzle._libs.doc
import sqlpuzzle._features.columns
import sqlpuzzle._features.groupby
import sqlpuzzle._features.having
import sqlpuzzle._features.intooutfile
import sqlpuzzle._features.limit
import sqlpuzzle._features.orderby
import sqlpuzzle._features.tables
import sqlpuzzle._features.where


class Select(sqlpuzzle._queries.Query):
    def __init__(self, *args, **kwds):
        """Initialization of Select."""
        super(Select, self).__init__()

        self._set_features(
            tables=sqlpuzzle._features.tables.TablesForSelect(),
            columns=sqlpuzzle._features.columns.Columns(),
            where=sqlpuzzle._features.where.Where(),
            group_by=sqlpuzzle._features.groupby.GroupBy(),
            having=sqlpuzzle._features.having.Having(),
            order_by=sqlpuzzle._features.orderby.OrderBy(),
            limit=sqlpuzzle._features.limit.Limit(),
            into_outfile=sqlpuzzle._features.intooutfile.IntoOutfile(),
            select_options=SelectOptions(),
        )
        self._set_keys_of_features_for_auto_printing(
            'tables', 'where', 'group_by', 'having', 'order_by', 'limit', 'into_outfile'
        )

        self.columns(*args, **kwds)

    def __str__(self):
        """Print query."""
        select_options = str(self._select_options)
        if select_options:
            select_options += ' '

        select = "SELECT %s%s" % (
            select_options,
            str(self._columns),
        )
        return super(Select, self)._print_features(select)

    def __and__(self, other):
        """UNION ALL selects."""
        return sqlpuzzle._queries.union.Union(self, other, sqlpuzzle._queries.union.UNION_ALL)

    def __or__(self, other):
        """UNION selects."""
        return sqlpuzzle._queries.union.Union(self, other, sqlpuzzle._queries.union.UNION)

    def columns(self, *args, **kwds):
        """Set column(s) to query."""
        self._columns.columns(*args, **kwds)
        return self

    def from_(self, *args, **kwds):
        """Set table(s) to query."""
        self._tables.set(*args, **kwds)
        return self

    def from_table(self, table, alias=None):
        """Set table to query."""
        self._tables.set((table, alias))
        return self

    def from_tables(self, *args, **kwds):
        """Alias for method `from_`."""
        self.from_(*args, **kwds)
        return self

    def join(self, table):
        """Join table."""
        self._tables.join(table)
        return self

    def inner_join(self, table):
        """Inner join table."""
        self._tables.inner_join(table)
        return self

    def left_join(self, table):
        """Left join table."""
        self._tables.left_join(table)
        return self

    def right_join(self, table):
        """Right join table."""
        self._tables.right_join(table)
        return self

    def on(self, *args, **kwds):
        """Join on."""
        self._tables.on(*args, **kwds)
        return self

    def where(self, *args, **kwds):
        """Set condition(s) of where to query."""
        self._where.where(*args, **kwds)
        return self

    def having(self, *args, **kwds):
        """Set condition(s) of having to query."""
        self._having.where(*args, **kwds)
        return self

    def group_by(self, *args, **kwds):
        """Set group to query."""
        self._group_by.group_by(*args, **kwds)
        return self

    def order_by(self, *args, **kwds):
        """Set order to query."""
        self._order_by.order_by(*args, **kwds)
        return self

    def limit(self, limit, offset=None):
        """Set limit (and offset)."""
        self._limit.limit(limit, offset)
        return self

    def offset(self, offset):
        """Set offset."""
        self._limit.offset(offset)
        return self

    def into_outfile(self, into_outfile):
        """Set INTO OUTFILE."""
        self._into_outfile.into_outfile(into_outfile)
        return self

    def fields_terminated_by(self, fields_terminated_by):
        """Set FIELDS TERMINATED BY."""
        self._into_outfile.fields_terminated_by(fields_terminated_by)
        return self

    def lines_terminated_by(self, lines_terminated_by):
        """Set LINES TERMINATED BY."""
        self._into_outfile.lines_terminated_by(lines_terminated_by)
        return self

    def optionally_enclosed_by(self, optionally_enclosed_by):
        """Set OPTIONALLY ENCLOSED BY."""
        self._into_outfile.optionally_enclosed_by(optionally_enclosed_by)
        return self

    # Broaden doc strings of functions by useful help.
    sqlpuzzle._libs.doc.doc(columns, 'columns')
    sqlpuzzle._libs.doc.doc(from_, 'tables')
    sqlpuzzle._libs.doc.doc(join, 'join')
    sqlpuzzle._libs.doc.doc(inner_join, 'join')
    sqlpuzzle._libs.doc.doc(left_join, 'join')
    sqlpuzzle._libs.doc.doc(right_join, 'join')
    sqlpuzzle._libs.doc.doc(on, 'where')
    sqlpuzzle._libs.doc.doc(where, 'where')
    sqlpuzzle._libs.doc.doc(having, 'where')
    sqlpuzzle._libs.doc.doc(group_by, 'order')
    sqlpuzzle._libs.doc.doc(order_by, 'order')
    sqlpuzzle._libs.doc.doc(limit, 'limit')

    # SELECT OPTIONS

    def sql_cache(self):
        """SQL_CACHE"""
        self._select_options.sql_cache()
        return self

    def sql_no_cache(self):
        """SQL_NO_CACHE"""
        self._select_options.sql_no_cache()
        return self

    def all(self):
        """ALL"""
        self._select_options.all()
        return self

    def distinct(self):
        """DISTINCT"""
        self._select_options.distinct()
        return self

    def distinctrow(self):
        """DISTINCTROW"""
        self._select_options.distinctrow()
        return self

    def sql_small_result(self, allow=True):
        """SQL_SMALL_RESULT"""
        self._select_options.sql_small_result(allow)
        return self

    def sql_big_result(self, allow=True):
        """SQL_BIG_RESULT"""
        self._select_options.sql_big_result(allow)
        return self

    def sql_buffer_result(self, allow=True):
        """SQL_BUFFER_RESULT"""
        self._select_options.sql_buffer_result(allow)
        return self

    def sql_calc_found_rows(self, allow=True):
        """SQL_CALC_FOUND_ROWS"""
        self._select_options.sql_calc_found_rows(allow)
        return self

    def straight_join(self, allow=True):
        """STRAIGHT_JOIN"""
        self._select_options.straight_join(allow)
        return self

    def high_priority(self, allow=True):
        """HIGH_PRIORITY"""
        self._select_options.high_priority(allow)
        return self


class SelectOptions(sqlpuzzle._libs.object.Object):
    _options = {
        'sql_cache': {
            'off': '',
            'cache': 'SQL_CACHE',
            'noCache': 'SQL_NO_CACHE'
        },
        'duplicated': {
            'off': '',
            'all': 'ALL',
            'distinct': 'DISTINCT',
            'distinctrow': 'DISTINCTROW',
        },
        'sql_small_result': {
            'off': '',
            'on': 'SQL_SMALL_RESULT',
        },
        'sql_big_result': {
            'off': '',
            'on': 'SQL_BIG_RESULT',
        },
        'sql_buffer_result': {
            'off': '',
            'on': 'SQL_BUFFER_RESULT',
        },
        'sql_calc_found_rows': {
            'off': '',
            'on': 'SQL_CALC_FOUND_ROWS',
        },
        'straight_join': {
            'off': '',
            'on': 'STRAIGHT_JOIN',
        },
        'high_priority': {
            'off': '',
            'on': 'HIGH_PRIORITY',
        },
    }

    def __init__(self):
        super(SelectOptions, self).__init__()
        self._set_options = {}
        for option_key in self._options.keys():
            self._set_options[option_key] = 'off'

    def copy(self):
        """Create copy."""
        new_select_options = self.__class__()
        new_select_options._set_options = dict(self._set_options)
        return new_select_options

    def __str__(self):
        return ' '.join(self._options[key][val] for key, val in self._set_options.iteritems() if val != 'off')

    def __eq__(self, other):
        """Are select options equivalent?"""
        if self.__class__ != other.__class__ or len(self._set_options) != len(other._set_options):
            return False
        return all(bool(so == oo) for so, oo in zip(self._set_options.values(), other._set_options.values()))

    def sql_cache(self):
        self._set_options['sql_cache'] = 'cache'

    def sql_no_cache(self):
        self._set_options['sql_cache'] = 'noCache'

    def all(self):
        self._set_options['duplicated'] = 'all'

    def distinct(self):
        self._set_options['duplicated'] = 'distinct'

    def distinctrow(self):
        self._set_options['duplicated'] = 'distinctrow'

    def sql_small_result(self, allow=True):
        self._set_options['sql_small_result'] = 'on' if allow else 'off'

    def sql_big_result(self, allow=True):
        self._set_options['sql_big_result'] = 'on' if allow else 'off'

    def sql_buffer_result(self, allow=True):
        self._set_options['sql_buffer_result'] = 'on' if allow else 'off'

    def sql_calc_found_rows(self, allow=True):
        self._set_options['sql_calc_found_rows'] = 'on' if allow else 'off'

    def straight_join(self, allow=True):
        self._set_options['straight_join'] = 'on' if allow else 'off'

    def high_priority(self, allow=True):
        self._set_options['high_priority'] = 'on' if allow else 'off'
