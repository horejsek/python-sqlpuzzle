# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six
from six.moves import xrange
try:
    long
except NameError:
    long = int

import types
import datetime

from sqlpuzzle._common import SqlValue, SqlReference, check_type_decorator, parse_args
from .queryparts import QueryPart, QueryParts, append_custom_sql_decorator
from sqlpuzzle import relations

__all__ = ('Condition', 'Conditions')


class Condition(QueryPart):
    _default_relations = {
        str: relations.EQ,
        six.text_type: relations.EQ,
        int: relations.EQ,
        long: relations.EQ,
        float: relations.EQ,
        bool: relations.EQ,
        list: relations.IN,
        tuple: relations.IN,
        xrange: relations.IN,
        types.GeneratorType: relations.IN,
        datetime.date: relations.EQ,
        datetime.datetime: relations.EQ,
        type(None): relations.IS,
    }

    def __init__(self, column_name, value):
        super(Condition, self).__init__()
        self.column_name = column_name
        self.value = value

    def __unicode__(self):
        foo = six.u('%(col)s %(rel)s %(val)s')

        value = self.value
        if isinstance(value, (list, tuple, xrange)) and None in value:
            value = [v for v in value if v is not None]
            # If list of values is empty, there must be only condition for NULL.
            if value:
                foo = six.u('(') + foo + six.u(' OR %(col)s IS NULL)')
            else:
                foo = '%(col)s IS NULL'

        return foo % {
            'col': SqlReference(self.column_name),
            'rel': self.relation,
            'val': self._get_value_for_str(value),
        }

    @staticmethod
    def _get_value_for_str(value):
        return SqlValue(value)

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
    @check_type_decorator(six.string_types)
    def column_name(self, column_name):
        self._column_name = column_name

    @property
    def value(self):
        return self._value.value

    @value.setter
    @check_type_decorator(six.string_types + six.integer_types + (
        float, bool, list, tuple, xrange, types.GeneratorType, datetime.date, datetime.datetime
    ))
    def value(self, value):
        if not isinstance(value, relations._RelationValue):
            value_type = type(value)
            value = self._default_relations.get(value_type, relations.EQ)(value)
        self._value = value

    @property
    def relation(self):
        return self._value.relation

    @property
    def relation_instance(self):
        return self._value



class Conditions(QueryParts):
    def __init__(self, condition_class=Condition):
        super(Conditions, self).__init__()
        self._condition_class = condition_class

    @append_custom_sql_decorator
    def where(self, *args, **kwds):
        options = {
            'min_items': 2,
            'max_items': 2,
            'allow_dict': True,
            'allow_list': True,
        }
        for column_name, value in parse_args(options, *args, **kwds):
            self.append_unique_part(self._condition_class(column_name, value))

        return self
