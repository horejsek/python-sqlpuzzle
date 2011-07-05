# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle._libs.argsParser
import sqlpuzzle._libs.sqlValue
import sqlpuzzle._features.features


class Column(object):
    def __init__(self, column=None, as_=None):
        """Initialization of Column."""
        self.column(column)
        self.as_(as_)
    
    def __str__(self):
        """Print part of query."""
        if self._as:
            return '%s AS "%s"' % (
                sqlpuzzle._libs.sqlValue.SqlReference(self._column),
                self._as,
            )
        else:
            return str(sqlpuzzle._libs.sqlValue.SqlReference(self._column))
    
    def __repr__(self):
        return "<Column: %s>" % self.__str__()
    
    def __eq__(self, other):
        """Are columns equivalent?"""
        return (
            self._column == other._column and
            self._as == other._as
        )
    
    def column(self, column):
        """Set column."""
        self._column = column
    
    def as_(self, as_):
        """Set as."""
        self._as = as_


class Columns(sqlpuzzle._features.features.Features):
    def __init__(self):
        """Initialization of Columns."""
        self._columns = []
    
    def __str__(self):
        """Print columns (part of query)."""
        if self.isSet():
            return ', '.join(str(column) for column in self._columns)
        else:
            return '*'
    
    def __repr__(self):
        return "<Columns: %s>" % self.__str__()
    
    def __contains__(self, item):
        """Is item (column) in columns?"""
        for column in self._columns:
            if item == column:
                return True
        return False
    
    def isSet(self):
        """Is limit set?"""
        return self._columns != []
    
    def columns(self, *args):
        """Set columns."""

        allowedDataTypes = sqlpuzzle._libs.argsParser.AllowedDataTypes().add(
            (str, unicode, sqlpuzzle._queries.select.Select, sqlpuzzle._queries.union.Union),
            (str, unicode)
        ).add(
            sqlpuzzle.customSql.CustomSql
        )

        for columnName, as_ in sqlpuzzle._libs.argsParser.parseArgsToListOfTuples(
            {'maxItems': 2, 'allowedDataTypes': allowedDataTypes}, *args
        ):
            if self.isCustumSql(columnName):
                self._columns.append(columnName)
            else:
                column = Column(columnName, as_)
                if column not in self:
                    self._columns.append(column)
        
        return self

