# -*- coding: utf-8 -*-

import six
import datetime

import sqlpuzzle._libs.argsparser
import sqlpuzzle._libs.sqlvalue


class Value(sqlpuzzle._features.Feature):
    def __init__(self, column=None, value=None):
        """Initialization of Value."""
        super(Value, self).__init__()
        self._column = column
        self._value = value

    def __str__(self):
        """Print part of query."""
        return '%s = %s' % (
            sqlpuzzle._libs.sqlvalue.SqlReference(self._column),
            sqlpuzzle._libs.sqlvalue.SqlValue(self._value),
        )

    def __eq__(self, other):
        """Are values equivalent?"""
        return (
            self._column == other._column and
            self._value == other._value
        )


class Values(sqlpuzzle._features.Features):
    def columns(self):
        """Print columns of values."""
        return ', '.join('%s' % sqlpuzzle._libs.sqlvalue.SqlReference(value._column) for value in self._features)

    def values(self, columnOrder=None):
        """Print values of values."""
        values = self._features
        if columnOrder:
            mapOfColumnsToValues = dict((value._column, value)
                                        for value in values)
            values = [mapOfColumnsToValues.get(column, None)
                      for column in columnOrder]
        return ', '.join('%s' % sqlpuzzle._libs.sqlvalue.SqlValue(value._value if value else None) for value in values)

    def set(self, *args, **kwds):
        """Set columns."""
        if args and self.is_custum_sql(args[0]):
            self._features.append(args[0])

        else:
            for columnName, value in sqlpuzzle._libs.argsparser.parse_args_to_list_of_tuples(
                {
                    'min_items': 2,
                    'max_items': 2,
                    'allow_dict': True,
                    'allow_list': True,
                    'allowed_data_types': (
                        six.string_types,
                        six.string_types + six.integer_types + (float, bool, datetime.date),
                    ),
                },
                *args, **kwds
            ):
                value = Value(columnName, value)
                if value not in self:
                    self._features.append(value)

        return self


class MultipleValues(sqlpuzzle._features.Features):
    def __str__(self):
        """Print part of query."""
        return '(%s) VALUES %s' % (
            self.columns(),
            self.values(),
        )

    @property
    def all_columns(self):
        """Return list of all columns."""
        columns = set()
        for values in self._features:
            for value in values._features:
                columns.add(value._column)
        return sorted(columns)

    def columns(self):
        """Print columns of values."""
        return ', '.join('%s' % sqlpuzzle._libs.sqlvalue.SqlReference(column) for column in self.all_columns)

    def values(self):
        """Print values of values."""
        column_order = self.all_columns
        return ', '.join('(%s)' % values.values(column_order) for values in self._features)

    def add(self, *args, **kwds):
        """Add new record."""
        values = Values().set(*args, **kwds)
        self._features.append(values)
        return self
