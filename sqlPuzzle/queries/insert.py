# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.queries.query

import sqlPuzzle.features.tables
import sqlPuzzle.features.onDuplicateKeyUpdate
import sqlPuzzle.features.values


class Insert(sqlPuzzle.queries.query.Query):
    def __init__(self):
        """Initialization of Insert."""
        super(Insert, self).__init__()
        
        self._setFeatures(
            tables = sqlPuzzle.features.tables.Tables(),
            values = sqlPuzzle.features.values.Values(),
            onDuplicateKeyUpdate = sqlPuzzle.features.onDuplicateKeyUpdate.OnDuplicateKeyUpdate(),
        )
        self._setPrintedFeatures('onDuplicateKeyUpdate')
    
    def __str__(self):
        """Print query."""
        insert = "INSERT INTO %s (%s) VALUES (%s)" % (
            str(self._tables),
            self._values.columns(),
            self._values.values(),
        )
        return sqlPuzzle.queries.query.Query._appendFeatures(self, insert)
    
    def __repr__(self):
        return "<Insert: %s>" % self.__str__()
    
    def _typeOfQuery(self):
        """Type of query."""
        return 'INSERT'
    
    def into(self, table):
        """Set table for insert."""
        self._tables.set(table)
        return self
    
    def values(self, *args, **kwds):
        """Set columns and values."""
        self._values.set(*args, **kwds)
        return self
    
    def onDuplicateKeyUpdate(self, *args, **kwds):
        """Set on duplicate key update."""
        self._onDuplicateKeyUpdate.set(*args, **kwds)
        return self

