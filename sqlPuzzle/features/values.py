# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import datetime

import sqlPuzzle.argsParser
import sqlPuzzle.sqlValue


class Values(object):
    def __init__(self):
        """
        Initialization of Values.
        """
        self._values = {}
    
    def __str__(self):
        """
        Print values (part of query).
        """
        return ', '.join(
            '`%s` = %s' % (column, str(sqlPuzzle.sqlValue.SqlValue(value)))
            for column, value in
            self._values.iteritems()
        )
    
    def __repr__(self):
        return "<Values: %s>" % self.__str__()
    
    def columns(self):
        """
        Print columns of values.
        """
        return ', '.join('`%s`' % column for column in self._values.keys())
    
    def values(self):
        """
        Print values of values.
        """
        return ', '.join('%s' % str(sqlPuzzle.sqlValue.SqlValue(value)) for value in self._values.values())
    
    def isSet(self):
        """
        Is limit set?
        """
        return self._values != {}
    
    def set(self, *args, **kwds):
        """
        Set columns.
        """
        self._values.update(dict(
            sqlPuzzle.argsParser.parseArgsToListOfTuples(
                {
                    'minItems': 2,
                    'maxItems': 2,
                    'allowDict': True,
                    'allowList': True,
                    'allowedDataTypes': ((str, unicode), (str, unicode, int, long, float, bool, datetime.date, datetime.datetime)),
                },
                *args, **kwds
            )
        ))
        return self

