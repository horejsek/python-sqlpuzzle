# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#


import sqlpuzzle.exceptions

import sqlpuzzle.queries.query
import sqlpuzzle.queries.select



UNION = 0
UNION_ALL = 1

UNION_TYPES = {
    UNION: 'UNION',
    UNION_ALL: 'UNION ALL',
}



class Union(sqlpuzzle.queries.query.Query):
    def __init__(self, query1, query2, unionType):
        self._setQuery1(query1)
        self._setQuery2(query2)
        self._setType(unionType)
    
    def _setQuery1(self, query):
        if not isinstance(query, (Union, sqlpuzzle.queries.select.Select)):
            raise sqlpuzzle.exceptions.InvalidArgumentException()
        self._query1 = query
    
    def _setQuery2(self, query):
        if not isinstance(query, (Union, sqlpuzzle.queries.select.Select)):
            raise sqlpuzzle.exceptions.InvalidArgumentException()
        self._query2 = query
    
    def _setType(self, type):
        if not type in UNION_TYPES.keys():
            raise sqlpuzzle.exceptions.InvalidArgumentException()
        self._type = type
    
    def __str__(self):
        """Print query."""
        return '%s %s %s' % (
            str(self._query1),
            UNION_TYPES[self._type],
            str(self._query2),
        )
    
    def __repr__(self):
        return "<Union: %s>" % self.__str__()
    
    def __and__(self, other):
        """UNION ALL"""
        return Union(self, other, UNION_ALL)
    
    def __or__(self, other):
        """UNION"""
        return Union(self, other, UNION)

