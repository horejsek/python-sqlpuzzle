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


class Delete(query.Query):
    def __init__(self):
        """
        Initialization of Delete.
        """
        query.Query.__init__(self)
        
        self._setExtensions(
            tables=tables.Tables(),
            conditions=conditions.Conditions(),
        )
        self._setPrintedExtensions('conditions')
        
        self.__allowDeleteAll = False
    
    def __str__(self):
        """
        Print query.
        """
        if not self._conditions.isSet() and not self.__allowDeleteAll:
            raise exceptions.ConfirmDeleteAllException()
        
        delete = "DELETE FROM %s" % (
            str(self._tables),
        )
        return query.Query._appendExtensions(self, delete)
    
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

