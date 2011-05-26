# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.exceptions
import sqlPuzzle.queries.query

import sqlPuzzle.extensions.conditions
import sqlPuzzle.extensions.tables


class Delete(sqlPuzzle.queries.query.Query):
    def __init__(self):
        """
        Initialization of Delete.
        """
        sqlPuzzle.queries.query.Query.__init__(self)
        
        self._setExtensions(
            tables = sqlPuzzle.extensions.tables.Tables(),
            conditions = sqlPuzzle.extensions.conditions.Conditions(),
        )
        self._setPrintedExtensions('conditions')
        
        self.__allowDeleteAll = False
    
    def __str__(self):
        """
        Print query.
        """
        if not self._conditions.isSet() and not self.__allowDeleteAll:
            raise sqlPuzzle.exceptions.ConfirmDeleteAllException()
        
        delete = "DELETE FROM %s" % (
            str(self._tables),
        )
        return sqlPuzzle.queries.query.Query._appendExtensions(self, delete)
    
    def allowDeleteAll(self):
        self.__allowDeleteAll = True
    
    def forbidDeleteAll(self):
        self.__allowDeleteAll = False
    
    def _typeOfQuery(self):
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
        self._conditions.where(*args, **kwds)
        return self

