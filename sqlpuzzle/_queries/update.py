# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle.exceptions

import sqlpuzzle._queries.query

import sqlpuzzle._features.tables
import sqlpuzzle._features.values
import sqlpuzzle._features.where


class Update(sqlpuzzle._queries.query.Query):
    def __init__(self, table=None):
        """Initialization of Update."""
        super(Update, self).__init__()
        
        self._setFeatures(
            tables = sqlpuzzle._features.tables.Tables(),
            values = sqlpuzzle._features.values.Values(),
            where = sqlpuzzle._features.where.Where(),
        )
        self._setPrintedFeatures('where')
        
        self.__allowUpdateAll = False
        
        self.table(table)
    
    def __str__(self):
        """Print query."""
        if not self._where.isSet() and not self.__allowUpdateAll:
            raise sqlpuzzle.exceptions.ConfirmUpdateAllException()
        
        update = "UPDATE %s SET %s" % (
            str(self._tables),
            str(self._values),
        )
        return sqlpuzzle._queries.query.Query._appendFeatures(self, update)
    
    def __repr__(self):
        return "<Update: %s>" % self.__str__()
    
    def _typeOfQuery(self):
        """Type of query."""
        return 'UPDATE'
    
    def allowUpdateAll(self):
        """Allow update all records."""
        self.__allowUpdateAll = True
        return self
    
    def forbidUpdateAll(self):
        """Forbid update all records."""
        self.__allowUpdateAll = False
        return self
    
    def table(self, table):
        """Set table."""
        self._tables.set(table)
        return self
    
    def set(self, *args, **kwds):
        """Set columns and values."""
        self._values.set(*args, **kwds)
        return self
    
    def where(self, *args, **kwds):
        """Set condition(s) to query."""
        self._where.where(*args, **kwds)
        return self

