# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle.exceptions
import sqlpuzzle._queries.query

import sqlpuzzle._features.tables
import sqlpuzzle._features.where


class Delete(sqlpuzzle._queries.query.Query):
    def __init__(self):
        """Initialization of Delete."""
        super(Delete, self).__init__()
        
        self._setFeatures(
            tables = sqlpuzzle._features.tables.Tables(),
            where = sqlpuzzle._features.where.Where(),
        )
        self._setPrintedFeatures('where')
        
        self.__allowDeleteAll = False
    
    def __str__(self):
        """Print query."""
        if not self._where.isSet() and not self.__allowDeleteAll:
            raise sqlpuzzle.exceptions.ConfirmDeleteAllException()
        
        delete = "DELETE FROM %s" % (
            str(self._tables),
        )
        return sqlpuzzle._queries.query.Query._appendFeatures(self, delete)
    
    def __repr__(self):
        return "<Delete: %s>" % self.__str__()
    
    def allowDeleteAll(self):
        """Allow delete all records."""
        self.__allowDeleteAll = True
        return self
    
    def forbidDeleteAll(self):
        """Forbid delete all records."""
        self.__allowDeleteAll = False
        return self
    
    def _typeOfQuery(self):
        """Type of query."""
        return 'DELETE'
    
    def from_(self, *tables):
        """Set table(s) to query."""
        self._tables.set(tables)
        return self
    
    def where(self, *args, **kwds):
        """Set condition(s) to query."""
        self._where.where(*args, **kwds)
        return self

