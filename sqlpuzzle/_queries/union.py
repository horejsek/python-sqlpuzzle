# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#


import sqlpuzzle.exceptions

import sqlpuzzle._queries.select



UNION = 0
UNION_ALL = 1

UNION_TYPES = {
    UNION: 'UNION',
    UNION_ALL: 'UNION ALL',
}



class Union(sqlpuzzle._queries.Query):
    def __init__(self, query1, query2, unionType):
        """Initialization of Union."""
        self._setQuery1(query1)
        self._setQuery2(query2)
        self._setType(unionType)
    
    def _setQuery1(self, query):
        """Set first query."""
        self._checkInstance(query)
        self._query1 = query
    
    def _setQuery2(self, query):
        """Set second query."""
        self._checkInstance(query)
        self._query2 = query
    
    def _checkInstance(self, query):
        """Check instance of query."""
        if not isinstance(query, (Union, sqlpuzzle._queries.select.Select)):
            raise sqlpuzzle.exceptions.InvalidArgumentException()
    
    def _setType(self, type):
        """Set type of union."""
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
    
    def __and__(self, other):
        """UNION ALL"""
        return Union(self, other, UNION_ALL)
    
    def __or__(self, other):
        """UNION"""
        return Union(self, other, UNION)

