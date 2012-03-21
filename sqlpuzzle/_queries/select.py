# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

import sqlpuzzle._queries.union

import sqlpuzzle._libs.doc
import sqlpuzzle._features.columns
import sqlpuzzle._features.groupBy
import sqlpuzzle._features.having
import sqlpuzzle._features.intoOutfile
import sqlpuzzle._features.limit
import sqlpuzzle._features.orderBy
import sqlpuzzle._features.tables
import sqlpuzzle._features.where


class Select(sqlpuzzle._queries.Query):
    def __init__(self, *args, **kwds):
        """Initialization of Select."""
        super(Select, self).__init__()

        self._setFeatures(
            tables = sqlpuzzle._features.tables.TablesForSelect(),
            columns = sqlpuzzle._features.columns.Columns(),
            where = sqlpuzzle._features.where.Where(),
            groupBy = sqlpuzzle._features.groupBy.GroupBy(),
            having = sqlpuzzle._features.having.Having(),
            orderBy = sqlpuzzle._features.orderBy.OrderBy(),
            limit = sqlpuzzle._features.limit.Limit(),
            intoOutfile = sqlpuzzle._features.intoOutfile.IntoOutfile(),
            selectOptions = SelectOptions(),
        )
        self._setKeysOfFeaturesForAutoPrinting('tables', 'where', 'groupBy', 'having', 'orderBy', 'limit', 'intoOutfile')

        self.columns(*args, **kwds)

    def __str__(self):
        """Print query."""
        selectOptions = str(self._selectOptions)
        if selectOptions:
            selectOptions += ' '

        select = "SELECT %s%s" % (
            selectOptions,
            str(self._columns),
        )
        return super(Select, self)._printFeatures(select)

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

    def fromTable(self, table, alias=None):
        """Set table to query."""
        self._tables.set((table, alias))
        return self

    def fromTables(self, *args, **kwds):
        """Alias for method `from_`."""
        self.from_(*args, **kwds)
        return self

    def join(self, table):
        """Join table."""
        self._tables.join(table)
        return self

    def innerJoin(self, table):
        """Inner join table."""
        self._tables.innerJoin(table)
        return self

    def leftJoin(self, table):
        """Left join table."""
        self._tables.leftJoin(table)
        return self

    def rightJoin(self, table):
        """Right join table."""
        self._tables.rightJoin(table)
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

    def groupBy(self, *args, **kwds):
        """Set group to query."""
        self._groupBy.groupBy(*args, **kwds)
        return self

    def orderBy(self, *args, **kwds):
        """Set order to query."""
        self._orderBy.orderBy(*args, **kwds)
        return self

    def limit(self, limit, offset=None):
        """Set limit (and offset)."""
        self._limit.limit(limit, offset)
        return self

    def offset(self, offset):
        """Set offset."""
        self._limit.offset(offset)
        return self

    def intoOutfile(self, intoOutfile):
        """Set INTO OUTFILE."""
        self._intoOutfile.intoOutfile(intoOutfile)
        return self

    def fieldsTerminatedBy(self, fieldsTerminatedBy):
        """Set FIELDS TERMINATED BY."""
        self._intoOutfile.fieldsTerminatedBy(fieldsTerminatedBy)
        return self

    def linesTerminatedBy(self, linesTerminatedBy):
        """Set LINES TERMINATED BY."""
        self._intoOutfile.linesTerminatedBy(linesTerminatedBy)
        return self

    def optionallyEnclosedBy(self, optionallyEnclosedBy):
        """Set OPTIONALLY ENCLOSED BY."""
        self._intoOutfile.optionallyEnclosedBy(optionallyEnclosedBy)
        return self

    # Broaden doc strings of functions by useful help.
    sqlpuzzle._libs.doc.doc(columns, 'columns')
    sqlpuzzle._libs.doc.doc(from_, 'tables')
    sqlpuzzle._libs.doc.doc(join, 'join')
    sqlpuzzle._libs.doc.doc(innerJoin, 'join')
    sqlpuzzle._libs.doc.doc(leftJoin, 'join')
    sqlpuzzle._libs.doc.doc(rightJoin, 'join')
    sqlpuzzle._libs.doc.doc(on, 'where')
    sqlpuzzle._libs.doc.doc(where, 'where')
    sqlpuzzle._libs.doc.doc(having, 'where')
    sqlpuzzle._libs.doc.doc(groupBy, 'order')
    sqlpuzzle._libs.doc.doc(orderBy, 'order')
    sqlpuzzle._libs.doc.doc(limit, 'limit')

    ### SELECT OPTIONS

    def sqlCache(self):
        """SQL_CACHE"""
        self._selectOptions.sqlCache()
        return self

    def sqlNoCache(self):
        """SQL_NO_CACHE"""
        self._selectOptions.sqlNoCache()
        return self

    def all(self):
        """ALL"""
        self._selectOptions.all()
        return self

    def distinct(self):
        """DISTINCT"""
        self._selectOptions.distinct()
        return self

    def distinctrow(self):
        """DISTINCTROW"""
        self._selectOptions.distinctrow()
        return self

    def sqlSmallResult(self, allow=True):
        """SQL_SMALL_RESULT"""
        self._selectOptions.sqlSmallResult(allow)
        return self

    def sqlBigResult(self, allow=True):
        """SQL_BIG_RESULT"""
        self._selectOptions.sqlBigResult(allow)
        return self

    def sqlBufferResult(self, allow=True):
        """SQL_BUFFER_RESULT"""
        self._selectOptions.sqlBufferResult(allow)
        return self

    def sqlCalcFoundRows(self, allow=True):
        """SQL_CALC_FOUND_ROWS"""
        self._selectOptions.sqlCalcFoundRows(allow)
        return self

    def straightJoin(self, allow=True):
        """STRAIGHT_JOIN"""
        self._selectOptions.straightJoin(allow)
        return self

    def highPriority(self, allow=True):
        """HIGH_PRIORITY"""
        self._selectOptions.highPriority(allow)
        return self



class SelectOptions(sqlpuzzle._libs.object.Object):
    _options = {
        'sqlCache': {
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
        'sqlSmallResult': {
            'off': '',
            'on': 'SQL_SMALL_RESULT',
        },
        'sqlBigResult': {
            'off': '',
            'on': 'SQL_BIG_RESULT',
        },
        'sqlBufferResult': {
            'off': '',
            'on': 'SQL_BUFFER_RESULT',
        },
        'sqlCalcFoundRows': {
            'off': '',
            'on': 'SQL_CALC_FOUND_ROWS',
        },
        'straightJoin': {
            'off': '',
            'on': 'STRAIGHT_JOIN',
        },
        'highPriority': {
            'off': '',
            'on': 'HIGH_PRIORITY',
        },
    }

    def __init__(self):
        self._setOptions = {}
        for optionKey in self._options.keys():
            self._setOptions[optionKey] = 'off'

    def copy(self):
        """Create copy."""
        newSelectOptions = self.__class__()
        newSelectOptions._setOptions = dict(self._setOptions)
        return newSelectOptions

    def __str__(self):
        return ' '.join(self._options[key][val] for key, val in self._setOptions.iteritems() if val != 'off')

    def __eq__(self, other):
        """Are select options equivalent?"""
        if self.__class__ != other.__class__ or len(self._setOptions) != len(other._setOptions):
            return False
        return all(bool(so == oo) for so, oo in zip(self._setOptions.values(), other._setOptions.values()))

    def sqlCache(self): self._setOptions['sqlCache'] = 'cache'
    def sqlNoCache(self): self._setOptions['sqlCache'] = 'noCache'
    def all(self): self._setOptions['duplicated'] = 'all'
    def distinct(self): self._setOptions['duplicated'] = 'distinct'
    def distinctrow(self): self._setOptions['duplicated'] = 'distinctrow'
    def sqlSmallResult(self, allow=True): self._setOptions['sqlSmallResult'] = 'on' if allow else 'off'
    def sqlBigResult(self, allow=True): self._setOptions['sqlBigResult'] = 'on' if allow else 'off'
    def sqlBufferResult(self, allow=True): self._setOptions['sqlBufferResult'] = 'on' if allow else 'off'
    def sqlCalcFoundRows(self, allow=True): self._setOptions['sqlCalcFoundRows'] = 'on' if allow else 'off'
    def straightJoin(self, allow=True): self._setOptions['straightJoin'] = 'on' if allow else 'off'
    def highPriority(self, allow=True): self._setOptions['highPriority'] = 'on' if allow else 'off'
