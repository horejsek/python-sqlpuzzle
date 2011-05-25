# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import query

import columns
import conditions
import groupBy
import limit
import orderBy
import tables


class Select(query.Query):
    def __init__(self, *columns_):
        """
        Initialization of Select.
        """
        query.Query.__init__(self)
        
        self._setExtensions(
            tables=tables.Tables(),
            columns=columns.Columns(),
            conditions=conditions.Conditions(),
            groupBy=groupBy.GroupBy(),
            orderBy=orderBy.OrderBy(),
            limit=limit.Limit(),
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
        return query.Query._appendExtensions(self, select)
    
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

