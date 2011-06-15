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
import sqlPuzzle.features.limit
import sqlPuzzle.features.orderBy
import sqlPuzzle.features.tables


class Select(sqlPuzzle.queries.query.Query):
    def __init__(self, *columns_):
        """
        Initialization of Select.
        """
        sqlPuzzle.queries.query.Query.__init__(self)
        
        self._setFeatures(
            tables = sqlPuzzle.features.tables.Tables(),
            columns = sqlPuzzle.features.columns.Columns(),
            conditions = sqlPuzzle.features.conditions.Conditions(),
            groupBy = sqlPuzzle.features.groupBy.GroupBy(),
            orderBy = sqlPuzzle.features.orderBy.OrderBy(),
            limit = sqlPuzzle.features.limit.Limit(),
        )
        self._setPrintedFeatures('conditions', 'groupBy', 'orderBy', 'limit')
        
        self.columns(*columns_)
    
    def __str__(self):
        """
        Print query.
        """
        select = "SELECT %s FROM %s" % (
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
        Set condition(s) to query.
        """
        self._conditions.where(*args, **kwds)
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

