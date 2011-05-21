# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import columns
import conditions
import limit
import groupBy
import orderBy
import tables


class Query:
    def __init__(self):
        """
        Initialization of Query.
        """
        self._tables = tables.Tables()
        self._columns = columns.Columns()
        self._conditions = conditions.Conditions()
        self._groupBy = groupBy.GroupBy()
        self._orderBy = orderBy.OrderBy()
        self._limit = limit.Limit()
    
    def __raiser(self, method):
        raise NotSupprotedException(method, self._typeOfQuery())
    
    def _typeOfQuery(self):
        return 'undefined'
    
    def from_(self, *args, **kwds): self.__raiser('from')
    def where(self, *args, **kwds): self.__raiser('where')
    def groupBy(self, *args, **kwds): self.__raiser('group by')
    def orderBy(self, *args, **kwds): self.__raiser('order by')
    def limit(self, *args, **kwds): self.__raiser('limit')
    def offset(self, *args, **kwds): self.__raiser('offset')
    def into(self, *args, **kwds): self.__raiser('into')
    def values(self, *args, **kwds): self.__raiser('values')
    def set(self, *args, **kwds): self.__raiser('values')


class NotSupprotedException(Exception):
    def __init__(self, method, typeOfQuery):
        self.method = method
        self.typeOfQuery = typeOfQuery
    
    def __str__(self):
        return "Method '%s' is not supported for type of query '%s'." % (
            self.method,
            self.typeOfQuery,
        )

