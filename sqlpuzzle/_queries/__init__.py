# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle._libs.object
import sqlpuzzle.exceptions

import sqlpuzzle._features.columns
import sqlpuzzle._features.conditions
import sqlpuzzle._features.groupBy
import sqlpuzzle._features.limit
import sqlpuzzle._features.orderBy
import sqlpuzzle._features.tables
import sqlpuzzle._features.values


class Query(sqlpuzzle._libs.object.Object):
    def __init__(self):
        """Initialization of Query."""
        self.__features = {}
        self.__printedFeatures = ()
    
    def __str__(self):
        """Print query."""
        return "abstract"
    
    
    def _printFeatures(self, prefix=''):
        """Append features into query."""
        query = str(prefix)
        for feature in self.__printedFeatures:
            object_ = self._getFeature(feature)
            if object_.isSet():
                query = '%s %s' % (query, object_)
        return query
    
    def _setFeatures(self, **kwds):
        """Set features."""
        self.__features = kwds
    
    def _setPrintedFeatures(self, *args):
        """Set features which is proposed to automatic print."""
        self.__printedFeatures = args
    
    def _getFeature(self, feature):
        """Get features."""
        if feature in self.__features:
            return self.__features[feature]
        self.__raiser(feature)
    
    
    @property
    def _tables(self): return self._getFeature('tables')
    
    @property
    def _columns(self): return self._getFeature('columns')
    
    @property
    def _values(self): return self._getFeature('values')
    
    @property
    def _onDuplicateKeyUpdate(self): return self._getFeature('onDuplicateKeyUpdate')
    
    @property
    def _where(self): return self._getFeature('where')
    
    @property
    def _groupBy(self): return self._getFeature('groupBy')
    
    @property
    def _having(self): return self._getFeature('having')
    
    @property
    def _orderBy(self): return self._getFeature('orderBy')
    
    @property
    def _limit(self): return self._getFeature('limit')
    
    @property
    def _intoOutfile(self): return self._getFeature('intoOutfile')
    
    
    def __and__(self, other): self.__raiser('union')
    def __or__(self, other): self.__raiser('union all')
    def columns(self, *args, **kwds): self.__raiser('columns')
    def from_(self, *args, **kwds): self.__raiser('from')
    def join(self, *args, **kwds): self.__raiser('from')
    def innerJoin(self, *args, **kwds): self.__raiser('innerJoin')
    def leftJoin(self, *args, **kwds): self.__raiser('leftJoin')
    def rightJoin(self, *args, **kwds): self.__raiser('rightJoin')
    def on(self, *args, **kwds): self.__raiser('on')
    def where(self, *args, **kwds): self.__raiser('where')
    def groupBy(self, *args, **kwds): self.__raiser('group by')
    def orderBy(self, *args, **kwds): self.__raiser('order by')
    def limit(self, *args, **kwds): self.__raiser('limit')
    def offset(self, *args, **kwds): self.__raiser('offset')
    def into(self, *args, **kwds): self.__raiser('into')
    def values(self, *args, **kwds): self.__raiser('values')
    def table(self, *args, **kwds): self.__raiser('table')
    def set(self, *args, **kwds): self.__raiser('set')
    
    
    def __raiser(self, method):
        """Raise if method is not implemented in actual instance."""
        raise sqlpuzzle.exceptions.NotSupprotedException(method, self.__class__.__name__)

