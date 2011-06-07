# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.exceptions

import sqlPuzzle.extensions.columns
import sqlPuzzle.extensions.conditions
import sqlPuzzle.extensions.groupBy
import sqlPuzzle.extensions.limit
import sqlPuzzle.extensions.orderBy
import sqlPuzzle.extensions.tables
import sqlPuzzle.extensions.values


class Query:
    def __init__(self):
        """
        Initialization of Query.
        """
        self.__extensions = {}
        self.__printedExtensions = ()
    
    def __raiser(self, method):
        raise sqlPuzzle.exceptions.NotSupprotedException(method, self._typeOfQuery())
    
    def _typeOfQuery(self):
        return 'undefined'
    
    def _appendExtensions(self, query=''):
        query = str(query)
        for extension in self.__printedExtensions:
            object_ = self._getExtension(extension)
            if object_.isSet():
                query = '%s %s' % (query, object_)
        return query
    
    def _setExtensions(self, **kwds):
        self.__extensions = kwds
    
    def _setPrintedExtensions(self, *args):
        self.__printedExtensions = args
    
    def _getExtension(self, extension):
        if extension in self.__extensions:
            return self.__extensions[extension]
        self.__raiser(extension)
    
    @property
    def _tables(self): return self._getExtension('tables')
    
    @property
    def _columns(self): return self._getExtension('columns')
    
    @property
    def _values(self): return self._getExtension('values')
    
    @property
    def _conditions(self): return self._getExtension('conditions')
    
    @property
    def _groupBy(self): return self._getExtension('groupBy')
    
    @property
    def _orderBy(self): return self._getExtension('orderBy')
    
    @property
    def _limit(self): return self._getExtension('limit')
    
    
    def columns(self, *args, **kwds): self.__raiser('columns')
    def from_(self, *args, **kwds): self.__raiser('from')
    def where(self, *args, **kwds): self.__raiser('where')
    def groupBy(self, *args, **kwds): self.__raiser('group by')
    def orderBy(self, *args, **kwds): self.__raiser('order by')
    def limit(self, *args, **kwds): self.__raiser('limit')
    def offset(self, *args, **kwds): self.__raiser('offset')
    def into(self, *args, **kwds): self.__raiser('into')
    def values(self, *args, **kwds): self.__raiser('values')
    def set(self, *args, **kwds): self.__raiser('values')

