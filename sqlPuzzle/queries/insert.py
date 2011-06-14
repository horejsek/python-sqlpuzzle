# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.queries.query

import sqlPuzzle.features.tables
import sqlPuzzle.features.values


class Insert(sqlPuzzle.queries.query.Query):
    def __init__(self):
        """
        Initialization of Insert.
        """
        sqlPuzzle.queries.query.Query.__init__(self)
        
        self._setFeatures(
            tables = sqlPuzzle.features.tables.Tables(),
            values = sqlPuzzle.features.values.Values(),
        )
    
    def __str__(self):
        """
        Print query.
        """
        insert = "INSERT INTO %s (%s) VALUES (%s)" % (
            str(self._tables),
            self._values.columns(),
            self._values.values(),
        )
        return insert
    
    def _typeOfQuery(self):
        """
        Type of query.
        """
        return 'INSERT'
    
    def into(self, table):
        """
        Set table for insert.
        """
        self._tables.set(table)
        return self
    
    def values(self, *args, **kwds):
        """
        Set columns and values.
        """
        self._values.set(*args, **kwds)
        return self

