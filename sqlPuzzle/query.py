# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import conditions
import limit
import tables


class Query:
    def __init__(self):
        """
        Initialization of Query.
        """
        self._tables = tables.Tables()
        self._conditions = conditions.Conditions()
        self._limit = limit.Limit()
    
    def __raiser(self, method):
        raise NotSupproted(method, self._typeOfQuery())
    
    def _typeOfQuery(self):
        return 'undefined'
    
    def limit(self, *args, **kwargs): self.__raiser('limit')
    def offset(self, *args, **kwargs): self.__raiser('offset')
    def from_(self, *args, **kwargs): self.__raiser('from')


class NotSupproted(Exception):
    def __init__(self, method, typeOfQuery):
        self.method = method
        self.typeOfQuery = typeOfQuery
    
    def __str__(self):
        return "Method '%s' is not supported for type of query '%s'." % (
            self.method,
            self.typeOfQuery,
        )

