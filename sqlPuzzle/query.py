# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import columns
import conditions
import exceptions
import groupBy
import limit
import orderBy
import tables
import values


class Query:
    def __init__(self):
        """
        Initialization of Query.
        """
        self._tables = tables.Tables()
        self._columns = columns.Columns()
        self._values = values.Values()
        self._conditions = conditions.Conditions()
        self._groupBy = groupBy.GroupBy()
        self._orderBy = orderBy.OrderBy()
        self._limit = limit.Limit()
    
    def __raiser(self, method):
        raise exceptions.NotSupprotedException(method, self._typeOfQuery())
    
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

