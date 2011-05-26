# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.queries.query

import sqlPuzzle.extensions.columns
import sqlPuzzle.extensions.conditions
import sqlPuzzle.extensions.groupBy
import sqlPuzzle.extensions.limit
import sqlPuzzle.extensions.orderBy
import sqlPuzzle.extensions.tables


class Select(sqlPuzzle.queries.query.Query):
    def __init__(self, *columns_):
        """
        Initialization of Select.
        """
        sqlPuzzle.queries.query.Query.__init__(self)
        
        self._setExtensions(
            tables = sqlPuzzle.extensions.tables.Tables(),
            columns = sqlPuzzle.extensions.columns.Columns(),
            conditions = sqlPuzzle.extensions.conditions.Conditions(),
            groupBy = sqlPuzzle.extensions.groupBy.GroupBy(),
            orderBy = sqlPuzzle.extensions.orderBy.OrderBy(),
            limit = sqlPuzzle.extensions.limit.Limit(),
        )
        self._setPrintedExtensions('conditions', 'groupBy', 'orderBy', 'limit')
        
        self.columns(*columns_)
    
    def __str__(self):
        """
        Print query.
        """
        select = "SELECT %s FROM %s" % (
            str(self._columns),
            str(self._tables),
        )
        return sqlPuzzle.queries.query.Query._appendExtensions(self, select)
    
    def _typeOfQuery(self):
        return 'SELECT'
    
    def columns(self, *columns_):
        """
        Set column(s) to query.
        """
        self._columns.columns(*columns_)
    
    def from_(self, *tables):
        """
        Set table(s) to query.
        """
        self._tables.set(tables)
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

