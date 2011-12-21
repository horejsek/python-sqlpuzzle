# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle._libs.sqlValue



class Function(object):
    def __init__(self, expr):
        self._expr = sqlpuzzle._libs.sqlValue.SqlReference(expr)
    
    def __str__(self):
        """Print some function, e.g. AVG, MAX, COUNT, ..."""
        return '<Function>'


class Avg(Function):
    def __str__(self):
        return 'AVG(%s)' % self._expr


class Count(Function):
    def __init__(self, expr=None):
        if not expr or expr == '*':
            self._expr = '*'
        else:
            self._expr = sqlpuzzle._libs.sqlValue.SqlValue(expr)

    def __str__(self):
        return 'COUNT(%s)' % self._expr


class Max(Function):
    def __str__(self):
        return 'MAX(%s)' % self._expr


class Min(Function):
    def __str__(self):
        return 'MIN(%s)' % self._expr


class Sum(Function):
    def __str__(self):
        return 'SUM(%s)' % self._expr

