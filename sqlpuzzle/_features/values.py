# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

import datetime

import sqlpuzzle._libs.argsParser
import sqlpuzzle._libs.sqlValue


class Value(sqlpuzzle._features.Feature):
    def __init__(self, column=None, value=None):
        """Initialization of Value."""
        self._column = column
        self._value = value
    
    def __str__(self):
        """Print part of query."""
        return '%s = %s' % (
            sqlpuzzle._libs.sqlValue.SqlReference(self._column),
            sqlpuzzle._libs.sqlValue.SqlValue(self._value),
        )
    
    def __eq__(self, other):
        """Are values equivalent?"""
        return (
            self._column == other._column and
            self._value == other._value
        )



class Values(sqlpuzzle._features.Features):
    def columns(self):
        """Print columns of values."""
        return ', '.join('%s' % sqlpuzzle._libs.sqlValue.SqlReference(value._column) for value in self._features)
    
    def values(self):
        """Print values of values."""
        return ', '.join('%s' % sqlpuzzle._libs.sqlValue.SqlValue(value._value) for value in self._features)
    
    def set(self, *args, **kwds):
        """Set columns."""
        if args and self.isCustumSql(args[0]):
            self._features.append(args[0])
        
        else:
            for columnName, value in sqlpuzzle._libs.argsParser.parseArgsToListOfTuples(
                {
                    'minItems': 2,
                    'maxItems': 2,
                    'allowDict': True,
                    'allowList': True,
                    'allowedDataTypes': ((str, unicode), (str, unicode, int, long, float, bool, datetime.date)),
                },
                *args, **kwds
            ):
                value = Value(columnName, value)
                if value not in self:
                    self._features.append(value)
            
        
        return self

