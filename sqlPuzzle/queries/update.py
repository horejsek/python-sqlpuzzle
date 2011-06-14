# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.exceptions

import sqlPuzzle.queries.query

import sqlPuzzle.features.conditions
import sqlPuzzle.features.tables
import sqlPuzzle.features.values


class Update(sqlPuzzle.queries.query.Query):
    def __init__(self, table=None):
        """
        Initialization of Update.
        """
        sqlPuzzle.queries.query.Query.__init__(self)
        
        self._setFeatures(
            tables = sqlPuzzle.features.tables.Tables(),
            values = sqlPuzzle.features.values.Values(),
            conditions = sqlPuzzle.features.conditions.Conditions(),
        )
        self._setPrintedFeatures('conditions')
        
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
        return sqlPuzzle.queries.query.Query._appendFeatures(self, update)
    
    def _typeOfQuery(self):
        """
        Type of query.
        """
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

