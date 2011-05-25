# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import query

import tables
import values


class Insert(query.Query):
    def __init__(self):
        """
        Initialization of Insert.
        """
        query.Query.__init__(self)
        
        self._setExtensions(
            tables=tables.Tables(),
            values=values.Values(),
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

