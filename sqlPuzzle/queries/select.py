# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.queries.query

import sqlPuzzle.features.columns
import sqlPuzzle.features.conditions
import sqlPuzzle.features.groupBy
import sqlPuzzle.features.having
import sqlPuzzle.features.intoOutfile
import sqlPuzzle.features.limit
import sqlPuzzle.features.orderBy
import sqlPuzzle.features.tables


class Select(sqlPuzzle.queries.query.Query):
    def __init__(self, *columns_):
        """
        Initialization of Select.
        """
        super(Select, self).__init__()
        
        self._setFeatures(
            tables = sqlPuzzle.features.tables.Tables(),
            columns = sqlPuzzle.features.columns.Columns(),
            conditions = sqlPuzzle.features.conditions.Conditions(),
            groupBy = sqlPuzzle.features.groupBy.GroupBy(),
            having = sqlPuzzle.features.having.Having(),
            orderBy = sqlPuzzle.features.orderBy.OrderBy(),
            limit = sqlPuzzle.features.limit.Limit(),
            intoOutfile = sqlPuzzle.features.intoOutfile.IntoOutfile(),
        )
        self._setPrintedFeatures('conditions', 'groupBy', 'having', 'orderBy', 'limit', 'intoOutfile')
        
        self._selectOptions = SelectOptions()
        
        self.columns(*columns_)
    
    def __str__(self):
        """
        Print query.
        """
        selectOptions = str(self._selectOptions)
        if selectOptions:
            selectOptions += ' '
        
        select = "SELECT %s%s FROM %s" % (
            selectOptions,
            str(self._columns),
            str(self._tables),
        )
        return sqlPuzzle.queries.query.Query._appendFeatures(self, select)
    
    def __repr__(self):
        return "<Select: %s>" % self.__str__()
    
    def _typeOfQuery(self):
        """
        Type of query.
        """
        return 'SELECT'
    
    def __and__(self, other):
        """
        UNION ALL selects.
        """
        return '%s UNION ALL %s' % (str(self), str(other))
    
    def __or__(self, other):
        """
        UNION selects.
        """
        return '%s UNION %s' % (str(self), str(other))
    
    def columns(self, *columns_):
        """
        Set column(s) to query.
        """
        self._columns.columns(*columns_)
        return self
    
    def from_(self, *tables):
        """
        Set table(s) to query.
        """
        self._tables.set(*tables)
        return self
    
    def join(self, table):
        """
        Join table.
        """
        self._tables.join(table)
        return self
    
    def innerJoin(self, table):
        """
        Inner join table.
        """
        self._tables.innerJoin(table)
        return self
    
    def leftJoin(self, table):
        """
        Left join table.
        """
        self._tables.leftJoin(table)
        return self
    
    def rightJoin(self, table):
        """
        Right join table.
        """
        self._tables.rightJoin(table)
        return self
    
    def on(self, *args, **kwds):
        """
        Join on.
        """
        self._tables.on(*args, **kwds)
        return self
    
    def where(self, *args, **kwds):
        """
        Set condition(s) of where to query.
        """
        self._conditions.where(*args, **kwds)
        return self
    
    def having(self, *args, **kwds):
        """
        Set condition(s) of having to query.
        """
        self._having.where(*args, **kwds)
        return self
    
    def groupBy(self, *args):
        """
        Set group to query.
        """
        self._groupBy.groupBy(*args)
        return self
    
    def orderBy(self, *args):
        """
        Set order to query.
        """
        self._orderBy.orderBy(*args)
        return self
    
    def limit(self, limit, offset=None):
        """
        Set limit (and offset).
        """
        self._limit.limit(limit, offset)
        return self
    
    def offset(self, offset):
        """
        Set offset.
        """
        self._limit.offset(offset)
        return self
    
    def intoOutfile(self, intoOutfile):
        """
        Set INTO OUTFILE.
        """
        self._intoOutfile.intoOutfile(intoOutfile)
        return self
    
    def fieldsTerminatedBy(self, fieldsTerminatedBy):
        """
        Set FIELDS TERMINATED BY.
        """
        self._intoOutfile.fieldsTerminatedBy(fieldsTerminatedBy)
        return self
    
    def linesTerminatedBy(self, linesTerminatedBy):
        """
        Set LINES TERMINATED BY.
        """
        self._intoOutfile.linesTerminatedBy(linesTerminatedBy)
        return self
    
    def optionallyEnclosedBy(self, optionallyEnclosedBy):
        """
        Set OPTIONALLY ENCLOSED BY.
        """
        self._intoOutfile.optionallyEnclosedBy(optionallyEnclosedBy)
        return self
    
    ### SELECT OPTIONS
    
    def sqlCache(self):
        """
        SQL_CACHE
        """
        self._selectOptions.sqlCache()
        return self
    
    def sqlNoCache(self):
        """
        SQL_NO_CACHE
        """
        self._selectOptions.sqlNoCache()
        return self
    
    def all(self):
        """
        ALL
        """
        self._selectOptions.all()
        return self
    
    def distinct(self):
        """
        DISTINCT
        """
        self._selectOptions.distinct()
        return self
    
    def distinctrow(self):
        """
        DISTINCTROW
        """
        self._selectOptions.distinctrow()
        return self
    
    def sqlSmallResult(self):
        """
        SQL_SMALL_RESULT
        """
        self._selectOptions.sqlSmallResult()
        return self
    
    def sqlBigResult(self):
        """
        SQL_BIG_RESULT
        """
        self._selectOptions.sqlBigResult()
        return self
    
    def sqlBufferResult(self):
        """
        SQL_BUFFER_RESULT
        """
        self._selectOptions.sqlBufferResult()
        return self
    
    def sqlCalcFoundRows(self):
        """
        SQL_CALC_FOUND_ROWS
        """
        self._selectOptions.sqlCalcFoundRows()
        return self
    
    def straightJoin(self):
        """
        STRAIGHT_JOIN
        """
        self._selectOptions.straightJoin()
        return self
    
    def highPriority(self):
        """
        HIGH_PRIORITY
        """
        self._selectOptions.highPriority()
        return self



class SelectOptions:
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
    
    def __str__(self):
        return ' '.join(self._options[key][val] for key, val in self._setOptions.iteritems() if val != 'off')
    
    def sqlCache(self): self._setOptions['sqlCache'] = 'cache'
    def sqlNoCache(self): self._setOptions['sqlCache'] = 'noCache'
    def all(self): self._setOptions['duplicated'] = 'all'
    def distinct(self): self._setOptions['duplicated'] = 'distinct'
    def distinctrow(self): self._setOptions['duplicated'] = 'distinctrow'
    def sqlSmallResult(self): self._setOptions['sqlSmallResult'] = 'on'
    def sqlBigResult(self): self._setOptions['sqlBigResult'] = 'on'
    def sqlBufferResult(self): self._setOptions['sqlBufferResult'] = 'on'
    def sqlCalcFoundRows(self): self._setOptions['sqlCalcFoundRows'] = 'on'
    def straightJoin(self): self._setOptions['straightJoin'] = 'on'
    def highPriority(self): self._setOptions['highPriority'] = 'on'


