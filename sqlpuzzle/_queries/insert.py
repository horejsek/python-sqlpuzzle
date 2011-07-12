# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle._libs.doc
import sqlpuzzle._features.tables
import sqlpuzzle._features.onDuplicateKeyUpdate
import sqlpuzzle._features.values


class Insert(sqlpuzzle._queries.Query):
    def __init__(self):
        """Initialization of Insert."""
        super(Insert, self).__init__()
        
        self._setFeatures(
            tables = sqlpuzzle._features.tables.Tables(),
            values = sqlpuzzle._features.values.Values(),
            onDuplicateKeyUpdate = sqlpuzzle._features.onDuplicateKeyUpdate.OnDuplicateKeyUpdate(),
        )
        self._setPrintedFeatures('onDuplicateKeyUpdate')
    
    def __str__(self):
        """Print query."""
        insert = "INSERT INTO %s (%s) VALUES (%s)" % (
            str(self._tables),
            self._values.columns(),
            self._values.values(),
        )
        return super(Insert, self)._printFeatures(insert)
    
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
    
    sqlpuzzle._libs.doc.doc(into, 'tables')
    sqlpuzzle._libs.doc.doc(values, 'values')

