# -*- coding: utf-8 -*-

import six
from six.moves import xrange
try:
    long
except NameError:
    long = int

import types
import datetime

import sqlpuzzle._libs.argsparser
import sqlpuzzle._libs.sqlvalue
import sqlpuzzle._queries
import sqlpuzzle.exceptions
import sqlpuzzle.relations


class Condition(sqlpuzzle._features.Feature):
    _default_relations = {
        str: sqlpuzzle.relations.EQ,
        six.text_type: sqlpuzzle.relations.EQ,
        int: sqlpuzzle.relations.EQ,
        long: sqlpuzzle.relations.EQ,
        float: sqlpuzzle.relations.EQ,
        bool: sqlpuzzle.relations.EQ,
        list: sqlpuzzle.relations.IN,
        tuple: sqlpuzzle.relations.IN,
        xrange: sqlpuzzle.relations.IN,
        types.GeneratorType: sqlpuzzle.relations.IN,
        datetime.date: sqlpuzzle.relations.EQ,
        datetime.datetime: sqlpuzzle.relations.EQ,
        type(None): sqlpuzzle.relations.IS,
        sqlpuzzle._queries.Query: sqlpuzzle.relations.EQ,
    }

    def __init__(self, column, value, relation=None):
        """Initialization of Condition."""
        super(Condition, self).__init__()
        self._column = column
        self._set_relation_value(value, relation)

    def _set_relation_value(self, value, relation):
        if isinstance(relation, type) and issubclass(relation, sqlpuzzle.relations._RelationValue):
            relation_value = relation(value)
        elif not isinstance(value, sqlpuzzle.relations._RelationValue):
            relation_value = self._create_default_relation_value(value)
        else:
            relation_value = value
        self._relation_value = relation_value

    def _create_default_relation_value(self, value):
        return self._default_relations[type(value)](value)

    def __str__(self):
        """Print condition (part of WHERE)."""
        foo = '%(col)s %(rel)s %(val)s'
        value = self._value
        if isinstance(value, (list, tuple, xrange)) and None in value:
            value = [v for v in value if v is not None]
            # If list of values is empty, there must be only condition for NULL.
            foo = '(' + foo + ' OR %(col)s IS NULL)' if value else '%(col)s IS NULL'
        return foo % {
            'col': sqlpuzzle._libs.sqlvalue.SqlReference(self._column),
            'rel': self._relation,
            'val': sqlpuzzle._libs.sqlvalue.SqlValue(value),
        }

    def __eq__(self, other):
        """Are conditions equivalent?"""
        return (
            self._column == other._column and
            self._relation_value == other._relation_value
        )

    @property
    def _value(self):
        return self._relation_value.value

    @property
    def _relation(self):
        return self._relation_value.relation


class Conditions(sqlpuzzle._features.Features):
    def __init__(self, condition_object=Condition):
        """Initialization of Conditions."""
        super(Conditions, self).__init__()
        self._condition_object = condition_object

    def where(self, *args, **kwds):
        """Set condition(s)."""
        if args and self.is_custum_sql(args[0]):
            self.append_feature(args[0])

        else:
            for column, value in sqlpuzzle._libs.argsparser.parse_args_to_list_of_tuples(
                {
                    'min_items': 2,
                    'max_items': 2,
                    'allow_dict': True,
                    'allow_list': True,
                    'allowed_data_types': (
                        six.string_types + (sqlpuzzle._queries.select.Select,),
                        six.string_types + six.integer_types + (
                            float, bool, list, tuple, xrange, types.GeneratorType, datetime.date,
                            datetime.datetime, sqlpuzzle.relations._RelationValue, sqlpuzzle._queries.select.Select,
                        ),
                        (sqlpuzzle.relations._RelationValue,)
                    ),
                },
                *args,
                **kwds
            ):
                condition = self._condition_object(column, value)
                if condition not in self:
                    self.append_feature(condition)

        return self
