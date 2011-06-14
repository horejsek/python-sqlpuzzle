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
import sqlPuzzle.extensions.values


class Update(sqlPuzzle.queries.query.Query):
    def __init__(self, table=None):
        """
        Initialization of Update.
        """
        sqlPuzzle.queries.query.Query.__init__(self)
        
        self._setExtensions(
            tables = sqlPuzzle.extensions.tables.Tables(),
            values = sqlPuzzle.extensions.values.Values(),
            conditions = sqlPuzzle.extensions.conditions.Conditions(),
        )
        self._setPrintedExtensions('conditions')
        
        self.__allowUpdateAll = False
        
        self.table(table)
    
    def __str__(self):
        """
        Print query.
        """
        if not self._conditions.isSet() and not self.__allowUpdateAll:
            raise sqlPuzzle.exceptions.ConfirmUpdateAllException()
        
        update = "UPDATE %s SET %s" % (
            str(self._tables),
            str(self._values),
        )
        return sqlPuzzle.queries.query.Query._appendExtensions(self, update)
    
    def _typeOfQuery(self):
        return 'UPDATE'
    
    def allowUpdateAll(self):
        """
        Allow update all records.
        """
        self.__allowUpdateAll = True
        return self
    
    def forbidUpdateAll(self):
        """
        Forbid update all records.
        """
        self.__allowUpdateAll = False
        return self
    
    def table(self, table):
        """
        Set table.
        """
        self._tables.set(table)
        return self
    
    def set(self, *args, **kwds):
        """
        Set columns and values.
        """
        self._values.set(*args, **kwds)
        return self
    
    def where(self, *args, **kwds):
        """
        Set condition(s) to query.
        """
        self._conditions.where(*args, **kwds)
        return self

