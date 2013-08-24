# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime
import six

from sqlpuzzle._common import SqlValue, SqlReference, is_sql_instance, check_type_decorator
from .queryparts import QueryPart, QueryParts, append_custom_sql_decorator

import sqlpuzzle._libs.argsparser


class Value(QueryPart):
    def __init__(self, column=None, value=None):
        super(Value, self).__init__()
        self.column_name = column
        self.value = value

    def __unicode__(self):
        return '%s = %s' % (
            SqlReference(self.column_name),
            SqlValue(self.value),
        )

    def __eq__(self, other):
        return (
            type(self) == type(other) and
            self.column_name == other.column_name and
            self.value == other.value
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
        return self._value

    @value.setter
    @check_type_decorator(six.string_types + six.integer_types + (type(None), float, bool, datetime.date))
    def value(self, value):
        self._value = value


class Values(QueryParts):
    @append_custom_sql_decorator
    def set(self, *args, **kwds):
        for column_name, value in sqlpuzzle._libs.argsparser.parse_args_to_list_of_tuples(
            {
                'min_items': 2,
                'max_items': 2,
                'allow_dict': True,
                'allow_list': True,
            },
            *args, **kwds
        ):
            self.append_unique_part(Value(column_name, value))

        return self

    def columns(self):
        return ', '.join(str(SqlReference(value.column_name)) for value in self._parts)

    def values(self, column_order=None):
        values = self._parts
        if column_order:
            map_of_col_to_val = dict((value.column_name, value) for value in values)
            values = [map_of_col_to_val.get(column, None) for column in column_order]
        return ', '.join(str(SqlValue(value.value if value else None)) for value in values)


class MultipleValues(QueryParts):
    def __unicode__(self):
        return '(%s) VALUES %s' % (
            self.columns(),
            self.values(),
        )

    @property
    def all_columns(self):
        """Return list of all columns."""
        columns = set()
        for values in self._parts:
            for value in values._parts:
                columns.add(value.column_name)
        return sorted(columns)

    def columns(self):
        return ', '.join(str(SqlReference(column)) for column in self.all_columns)

    def values(self):
        column_order = self.all_columns
        return ', '.join('(%s)' % values.values(column_order) for values in self._parts)

    def add(self, *args, **kwds):
        values = Values().set(*args, **kwds)
        self.append_part(values)
        return self
