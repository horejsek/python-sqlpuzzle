# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle._libs.object
import sqlpuzzle._libs.sqlValue

import sqlpuzzle._features.orderBy



class Function(sqlpuzzle._libs.object.Object):
    _functionName = None

    def __init__(self, expr):
        self._expr = sqlpuzzle._libs.sqlValue.SqlReference(expr)

    def __str__(self):
        if not self._functionName:
            return '<Function>'
        return '%s(%s)' % (
            self._functionName,
            self._expr,
        )



class FunctionWithDistinct(Function):
    def __init__(self, expr, distinct=False):
        super(FunctionWithDistinct, self).__init__(expr)
        self.distinct(distinct)

    def distinct(self, distinct=True):
        """Set DISTINCT."""
        self._distinct = bool(distinct)
        return self

    def __str__(self):
        if not self._functionName:
            return '<FunctionWithDistinct>'
        return '%s(%s%s)' % (
            self._functionName,
            self._strDistinct(),
            self._expr,
        )

    def _strDistinct(self):
        return 'DISTINCT ' if self._distinct else ''



class Avg(FunctionWithDistinct):
    _functionName = 'AVG'



class Count(FunctionWithDistinct):
    _functionName = 'COUNT'

    def __init__(self, expr=None, distinct=False):
        if not expr or expr == '*':
            self._expr = '*'
        else:
            self._expr = sqlpuzzle._libs.sqlValue.SqlReference(expr)

        self.distinct(distinct)



class Max(FunctionWithDistinct):
    _functionName = 'MAX'



class Min(FunctionWithDistinct):
    _functionName = 'MIN'



class Sum(FunctionWithDistinct):
    _functionName = 'SUM'



class GroupConcat(Function):
    _functionName = 'GROUP_CONCAT'

    def __init__(self, *expr):
        self._columns = sqlpuzzle._features.columns.Columns().columns(*expr)
        if not self._columns.isSet():
            raise sqlpuzzle.exceptions.InvalidArgumentException('You must specify columns for GROUP_CONCAT.')

        self._orderBy = sqlpuzzle._features.orderBy.OrderBy()
        self._separator = None

    def __str__(self):
        return '%s(%s%s%s)' % (
            self._functionName,
            self._columns,
            self._strOrderBy(),
            self._strSeparator(),
        )

    def _strOrderBy(self):
        if self._orderBy.isSet():
            return ' %s' % self._orderBy
        return ''

    def _strSeparator(self):
        if self._separator:
            return ' SEPARATOR %s' % sqlpuzzle._libs.sqlValue.SqlValue(self._separator)
        return ''

    def orderBy(self, *args):
        self._orderBy.orderBy(*args)
        return self

    def separator(self, separator):
        self._separator = separator
        return self