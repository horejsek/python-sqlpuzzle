# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import exceptions
import query

import conditions
import tables
import values


class Update(query.Query):
    def __init__(self, table=None):
        """
        Initialization of Update.
        """
        query.Query.__init__(self)
        
        self._setExtensions(
            tables=tables.Tables(),
            values=values.Values(),
            conditions=conditions.Conditions(),
        )
        self._setPrintedExtensions('conditions')
        
        self.__allowUpdateAll = False
        
        self.table(table)
    
    def __str__(self):
        """
        Print query.
        """
        if not self._conditions.isSet() and not self.__allowUpdateAll:
            raise exceptions.ConfirmUpdateAllException()
        
        update = "UPDATE %s SET %s" % (
            str(self._tables),
            str(self._values),
        )
        return query.Query._appendExtensions(self, update)
    
    def _typeOfQuery(self):
        return 'UPDATE'
    
    def allowUpdateAll(self):
        self.__allowUpdateAll = True
    
    def forbidUpdateAll(self):
        self.__allowUpdateAll = False
    
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

