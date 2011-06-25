# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.exceptions
import sqlPuzzle.queries.query

import sqlPuzzle.features.tables
import sqlPuzzle.features.where


class Delete(sqlPuzzle.queries.query.Query):
    def __init__(self):
        """
        Initialization of Delete.
        """
        super(Delete, self).__init__()
        
        self._setFeatures(
            tables = sqlPuzzle.features.tables.Tables(),
            where = sqlPuzzle.features.where.Where(),
        )
        self._setPrintedFeatures('where')
        
        self.__allowDeleteAll = False
    
    def __str__(self):
        """
        Print query.
        """
        if not self._where.isSet() and not self.__allowDeleteAll:
            raise sqlPuzzle.exceptions.ConfirmDeleteAllException()
        
        delete = "DELETE FROM %s" % (
            str(self._tables),
        )
        return sqlPuzzle.queries.query.Query._appendFeatures(self, delete)
    
    def __repr__(self):
        return "<Delete: %s>" % self.__str__()
    
    def allowDeleteAll(self):
        """
        Allow delete all records.
        """
        self.__allowDeleteAll = True
        return self
    
    def forbidDeleteAll(self):
        """
        Forbid delete all records.
        """
        self.__allowDeleteAll = False
        return self
    
    def _typeOfQuery(self):
        """
        Type of query.
        """
        return 'DELETE'
    
    def from_(self, *tables):
        """
        Set table(s) to query.
        """
        self._tables.set(tables)
        return self
    
    def where(self, *args, **kwds):
        """
        Set condition(s) to query.
        """
        self._where.where(*args, **kwds)
        return self

