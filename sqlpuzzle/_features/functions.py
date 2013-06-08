# -*- coding: utf-8 -*-

import re

import sqlpuzzle._libs.object
import sqlpuzzle._libs.sqlvalue

import sqlpuzzle._features.orderby


class Function(sqlpuzzle._libs.object.Object):
    _function_name = None

    def __init__(self, expr):
        super(Function, self).__init__()
        self._expr = sqlpuzzle._libs.sqlvalue.SqlReference(expr)

    def __str__(self):
        if not self._function_name:
            return '<Function>'
        return '%s(%s)' % (
            self._function_name,
            self._expr,
        )

    @property
    def _expr(self):
        return self.__expr

    @_expr.setter
    def _expr(self, expr):
        self.__expr = expr


class FunctionWithDistinct(Function):
    def __init__(self, expr, distinct=False):
        super(FunctionWithDistinct, self).__init__(expr)
        self.distinct(distinct)

    def distinct(self, distinct=True):
        """Set DISTINCT."""
        self._distinct = bool(distinct)
        return self

    def __str__(self):
        if not self._function_name:
            return '<FunctionWithDistinct>'
        return '%s(%s%s)' % (
            self._function_name,
            self._strDistinct(),
            self._expr,
        )

    def _strDistinct(self):
        return 'DISTINCT ' if self._distinct else ''


class Avg(FunctionWithDistinct):
    _function_name = 'AVG'


class Count(FunctionWithDistinct):
    _function_name = 'COUNT'

    def __init__(self, expr=None, distinct=False):
        if not expr or expr == '*':
            self._expr = '*'
        else:
            if not isinstance(expr, (list, tuple)):
                expr = (expr,)
            self._expr = (sqlpuzzle._libs.sqlvalue.SqlReference(e)
                          for e in expr)

        self.distinct(distinct)

    @Function._expr.getter
    def _expr(self):
        expr = Function._expr.fget(self)
        return ', '.join(str(e) for e in expr)


class Max(FunctionWithDistinct):
    _function_name = 'MAX'


class Min(FunctionWithDistinct):
    _function_name = 'MIN'


class Sum(FunctionWithDistinct):
    _function_name = 'SUM'


class Concat(Function):
    _function_name = 'CONCAT'

    def __init__(self, *expr):
        self._columns = sqlpuzzle._features.columns.Columns().columns(*expr)
        if not self._columns.is_set():
            raise sqlpuzzle.exceptions.InvalidArgumentException(
                'You must specify columns for %s.' % self._function_name)

    def __str__(self):
        return '%s(%s)' % (
            self._function_name,
            self._columns,
        )


class GroupConcat(Concat):
    _function_name = 'GROUP_CONCAT'

    def __init__(self, *expr):
        super(GroupConcat, self).__init__(*expr)
        self._order_by = sqlpuzzle._features.orderby.OrderBy()
        self._separator = None

    def __str__(self):
        return '%s(%s%s%s)' % (
            self._function_name,
            self._columns,
            self._str_order_by(),
            self._str_separator(),
        )

    def _str_order_by(self):
        if self._order_by.is_set():
            return ' %s' % self._order_by
        return ''

    def _str_separator(self):
        if self._separator:
            return ' SEPARATOR %s' % sqlpuzzle._libs.sqlvalue.SqlValue(self._separator)
        return ''

    def order_by(self, *args):
        self._order_by.order_by(*args)
        return self

    def separator(self, separator):
        self._separator = separator
        return self


class Convert(Function):
    _function_name = 'CONVERT'
    _allowed_types = ('BINARY', 'CHAR', 'DATE', 'DATETIME', 'DECIMAL', 'SIGNED', 'TIME', 'UNSIGNED')

    def __init__(self, expr, type_=None):
        super(Convert, self).__init__(expr)
        self._type = None
        if type_:
            self.to(type_)

    def __str__(self):
        return '%s(%s, %s)' % (
            self._function_name,
            self._expr,
            self._type,
        )

    def to(self, type_):
        type_ = str(type_).upper()
        self._check_type(type_)

        self._type = type_
        return self

    def _check_type(self, type_):
        type_ = type_.split('(')

        type_name = type_[0].strip()
        if type_name not in self._allowed_types:
            raise sqlpuzzle.exceptions.InvalidArgumentException(
                'You can convert value only into this types: %s' % repr(self._allowed_types))

        if len(type_) > 2 or (len(type_) == 2 and type_[1][-1] != ')'):
            raise sqlpuzzle.exceptions.InvalidArgumentException(
                'Invalid type in function %s.' % self._function_name)

        if len(type_) == 2 and not re.match('^[0-9]+(,[0-9]+)?\)$', type_[1]):
            raise sqlpuzzle.exceptions.InvalidArgumentException(
                'In function %s you can set as param of type only the number.' % self._function_name)
