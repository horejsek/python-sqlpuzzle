# -*- coding: utf-8 -*-

import sqlpuzzle.exceptions

import sqlpuzzle._queries.select


UNION = 0
UNION_ALL = 1

UNION_TYPES = {
    UNION: 'UNION',
    UNION_ALL: 'UNION ALL',
}


class Union(sqlpuzzle._queries.Query):
    def __init__(self, query1, query2, union_type):
        """Initialization of Union."""
        super(Union, self).__init__()
        self._set_query1(query1)
        self._set_query2(query2)
        self._set_type(union_type)

    def _set_query1(self, query):
        """Set first query."""
        self._check_instance(query)
        self._query1 = query

    def _set_query2(self, query):
        """Set second query."""
        self._check_instance(query)
        self._query2 = query

    def _check_instance(self, query):
        """Check instance of query."""
        if not isinstance(query, (Union, sqlpuzzle._queries.select.Select)):
            raise sqlpuzzle.exceptions.InvalidArgumentException()

    def _set_type(self, type):
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

    def __eq__(self, other):
        """Are queries equivalent?"""
        return (
            self.__class__ == other.__class__ and
            self._query1 == other._query1 and
            self._query2 == other._query2 and
            self._type == other._type
        )

    def __and__(self, other):
        """UNION ALL"""
        return Union(self, other, UNION_ALL)

    def __or__(self, other):
        """UNION"""
        return Union(self, other, UNION)
