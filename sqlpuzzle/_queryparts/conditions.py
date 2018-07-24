import datetime
import decimal
import types

from sqlpuzzle._common import Object, SqlValue, SqlReference, check_type_decorator, parse_args
from sqlpuzzle import relations
from .functions import Function
from .queryparts import QueryPart, QueryParts, append_custom_sql_decorator

__all__ = ('Condition', 'Conditions', 'Not')


class BinaryOperationMixin:
    AND = 'AND'
    OR = 'OR'

    def __and__(self, other):
        if not isinstance(other, (Condition, Conditions, ConditionsOfConditions)):
            raise TypeError(other)
        return ConditionsOfConditions(self, other, self.AND)

    def __or__(self, other):
        if not isinstance(other, (Condition, Conditions, ConditionsOfConditions)):
            raise TypeError(other)
        return ConditionsOfConditions(self, other, self.OR)


class Condition(BinaryOperationMixin, QueryPart):
    _default_relations = {
        str: relations.EQ,
        int: relations.EQ,
        float: relations.EQ,
        decimal.Decimal: relations.EQ,
        bool: relations.EQ,
        list: relations.IN,
        tuple: relations.IN,
        range: relations.IN,
        types.GeneratorType: relations.IN,
        datetime.date: relations.EQ,
        datetime.datetime: relations.EQ,
        type(None): relations.IS,
    }

    def __init__(self, column_name, value):
        super().__init__()
        self.column_name = column_name
        self.value = value

    def __str__(self):
        return self._value._format_condition(SqlReference(self.column_name), value_transformer=SqlValue)

    def __eq__(self, other):
        return (
            type(self) == type(other) and
            self.column_name == other.column_name and
            self.value == other.value and
            self.relation == other.relation
        )

    @property
    def column_name(self):
        return self._column_name

    @column_name.setter
    @check_type_decorator(str)
    def column_name(self, column_name):
        self._column_name = column_name

    @property
    def value(self):
        return self._value.value

    @value.setter
    @check_type_decorator((
        type(None), str, int, float, decimal.Decimal, bool, list, tuple,
        range, types.GeneratorType, datetime.date, datetime.datetime,
    ))
    def value(self, value):
        if not isinstance(value, relations._RelationValue):
            value_type = type(value.value if isinstance(value, SqlValue) else value)
            value = self._default_relations.get(value_type, relations.EQ)(value)
        self._value = value

    @property
    def relation(self):
        return self._value.relation

    @property
    def relation_instance(self):
        return self._value


class Conditions(BinaryOperationMixin, QueryParts):
    _separator_of_parts = ' AND '
    _condition_class = Condition

    def __init__(self, *args, **kwds):
        super().__init__()
        self.where(*args, **kwds)

    @append_custom_sql_decorator
    def where(self, *args, **kwds):
        options = {
            'min_items': 2,
            'max_items': 2,
            'allow_dict': True,
            'allow_list': True,
        }
        if args and all(isinstance(item, (Conditions, ConditionsOfConditions)) for item in args):
            for item in args:
                self.append_unique_part(item)
        else:
            for column_name, value in parse_args(options, *args, **kwds):
                self.append_unique_part(self._condition_class(column_name, value))

        return self


class ConditionsOfConditions(BinaryOperationMixin, Object):
    def __init__(self, left, right, type_):
        self.left = left
        self.right = right
        self.type = type_

    def __str__(self):
        template = '('
        template += '({})' if self._needs_brackets(self.left) else '{}'
        template += ' {} '
        template += '({})' if self._needs_brackets(self.right) else '{}'
        template += ')'
        return template.format(self.left, self.type, self.right)

    @staticmethod
    def _needs_brackets(value):
        return isinstance(value, QueryParts) and value.count_of_parts > 1


class Not(Function):
    _function_name = 'NOT'

    def __init__(self, *args, **kwds):
        expr = Conditions(*args, **kwds)
        super().__init__(expr)
