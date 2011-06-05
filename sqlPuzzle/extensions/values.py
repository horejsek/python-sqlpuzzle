# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.argsParser
import sqlPuzzle.sqlValue


class Values:
    def __init__(self):
        """
        Initialization of Values.
        """
        self.__values = {}
    
    def __str__(self):
        """
        Print values (part of query).
        """
        return ', '.join('`%s` = %s' % (column, str(sqlPuzzle.sqlValue.SqlValue(value))) for column, value in self.__values.iteritems())
    
    def columns(self):
        """
        Print columns of values.
        """
        return ', '.join('`%s`' % column for column in self.__values.keys())
    
    def values(self):
        """
        Print values of values.
        """
        return ', '.join('%s' % str(sqlPuzzle.sqlValue.SqlValue(value)) for value in self.__values.values())
    
    def isSet(self):
        """
        Is limit set?
        """
        return self.__values != {}
    
    def set(self, *args, **kwds):
        """
        Set columns.
        """
        self.__values.update(dict(
            sqlPuzzle.argsParser.parseArgsToListOfTuples(
                {'minItems': 2, 'maxItems': 2, 'allowDict': True, 'allowList': True}, *args, **kwds
            )
        ))
        return self

