# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle._libs.object
import sqlpuzzle._libs.sqlValue



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
