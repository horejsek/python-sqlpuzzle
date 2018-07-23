from sqlpuzzle._common import Object, SqlReference, SqlValue, force_text
from sqlpuzzle.exceptions import InvalidArgumentException
from .columns import Columns
from .orderby import OrderBy

__all__ = (
    'Avg',
    'Count',
    'Max',
    'Min',
    'Sum',
    'Concat',
    'GroupConcat',
    'Convert',
)


class Function(Object):
    _function_name = None

    def __init__(self, expr):
        super(Function, self).__init__()
        self.expr = expr

    def __unicode__(self):
        if not self._function_name:
            return '<Function>'
        return '%s(%s)' % (
            self._function_name,
            self._get_expr_as_string(),
        )

    def _get_expr_as_string(self):
        if isinstance(self.expr, (list, tuple)):
            return ', '.join(force_text(SqlReference(e)) for e in self.expr)
        return SqlReference(self.expr)

    @property
    def expr(self):
        return self._expr

    @expr.setter
    def expr(self, expr):
        self._expr = expr


class FunctionWithDistinct(Function):
    def __init__(self, expr, distinct=False):
        super(FunctionWithDistinct, self).__init__(expr)
        self.distinct(distinct)

    def distinct(self, distinct=True):
        self._distinct = bool(distinct)
        return self

    def __unicode__(self):
        if not self._function_name:
            return '<FunctionWithDistinct>'
        return '%s(%s%s)' % (
            self._function_name,
            'DISTINCT ' if self._distinct else '',
            self._get_expr_as_string(),
        )


class Avg(FunctionWithDistinct):
    _function_name = 'AVG'


class Count(FunctionWithDistinct):
    _function_name = 'COUNT'

    def __init__(self, expr=None, distinct=False):
        if not expr:
            expr = '*'
        super(Count, self).__init__(expr, distinct)

    def _get_expr_as_string(self):
        if self.expr == '*':
            return self.expr
        return super(Count, self)._get_expr_as_string()


class Max(FunctionWithDistinct):
    _function_name = 'MAX'


class Min(FunctionWithDistinct):
    _function_name = 'MIN'


class Sum(FunctionWithDistinct):
    _function_name = 'SUM'


class Concat(Function):
    _function_name = 'CONCAT'

    def __init__(self, *expr):
        self._columns = Columns().columns(*expr)
        if not self._columns.is_set:
            raise InvalidArgumentException('You must specify columns for %s.' % self._function_name)

    def __unicode__(self):
        return '%s(%s)' % (
            self._function_name,
            self._columns,
        )


class GroupConcat(Concat):
    _function_name = 'GROUP_CONCAT'

    def __init__(self, *expr):
        super(GroupConcat, self).__init__(*expr)
        self._order_by = OrderBy()
        self._separator = None

    def __unicode__(self):
        return '%s(%s%s%s)' % (
            self._function_name,
            self._columns,
            self._str_order_by(),
            self._str_separator(),
        )

    def _str_order_by(self):
        if self._order_by.is_set:
            return ' %s' % self._order_by
        return ''

    def _str_separator(self):
        if self._separator:
            return ' SEPARATOR %s' % SqlValue(self._separator)
        return ''

    def order_by(self, *args):
        """
        Order of concatination.

        .. code-block:: python

            >>> sqlpuzzle.group_concat('col').order_by('col')
            <GroupConcat: GROUP_CONCAT("col" ORDER BY "col")>
        """
        self._order_by.order_by(*args)
        return self

    def separator(self, separator):
        """
        Separator of values.

        .. code-block:: python

            >>> sqlpuzzle.group_concat('col').separator('-')
            <GroupConcat: GROUP_CONCAT("col" SEPARATOR '-')>
        """
        self._separator = separator
        return self


class Convert(Function):
    _function_name = 'CONVERT'

    def __init__(self, expr, type_=None):
        super(Convert, self).__init__(expr)
        self._type = None
        if type_:
            self.to(type_)

    def __unicode__(self):
        return '%s(%s, %s)' % (
            self._function_name,
            self._get_expr_as_string(),
            self._type,
        )

    def to(self, type_):
        """
        Convert to which type.

        .. code-block:: python

            >>> sqlpuzzle.convert('col').to('unsigned')
            <Convert: CONVERT("col", UNSIGNED)>

            >>> sqlpuzzle.convert('col', 'unsigned')
            <Convert: CONVERT("col", UNSIGNED)>
        """
        self._type = str(type_).upper()
        return self
