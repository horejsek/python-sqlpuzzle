# -*- coding: utf-8 -*-

import six
from six.moves import xrange

import types
import datetime

import sqlpuzzle._libs.object
from sqlpuzzle._libs.customsql import CustomSql
from sqlpuzzle._queries import Query


class _RelationValue(sqlpuzzle._libs.object.Object):
    _string_representation = 'Abstract Relation'
    _allowed_types = ()

    def __init__(self, value):
        super(_RelationValue, self).__init__()
        self._check_value_type(value)
        self._value = value

    def __str__(self):
        return '"%s %s"' % (
            self._string_representation,
            self._value,
        )

    def __eq__(self, other):
        """Are relations equivalent?"""
        return (
            self.__class__ == other.__class__ and
            self._value == other._value
        )

    def _check_value_type(self, value):
        # isinstance(True, (int, long)) is True => must be special condition
        if (
            (bool not in self._allowed_types and isinstance(value, bool)) or
            not isinstance(value, self._allowed_types)
        ):
            raise sqlpuzzle.exceptions.InvalidArgumentException(
                'Relation "%s" is not allowed for data type "%s".' % (
                    self._string_representation,
                    type(value)
                )
            )

    @property
    def relation(self):
        return self._string_representation

    @property
    def value(self):
        return self._value


class EQ(_RelationValue):
    _string_representation = '='
    _allowed_types = six.string_types + six.integer_types + (float, bool, datetime.date, Query, CustomSql)
EQUAL_TO = EQ


class NE(EQ):
    _string_representation = '!='
NOT_EQUAL_TO = NE


class GT(_RelationValue):
    _string_representation = '>'
    _allowed_types = six.integer_types + (float, datetime.date, Query, CustomSql)
GRATHER_THAN = GT


class GE(GT):
    _string_representation = '>='
GRATHER_THAN_OR_EQUAL_TO = GE


class LT(GT):
    _string_representation = '<'
LESS_THAN = LT


class LE(GT):
    _string_representation = '<='
LESS_THAN_OR_EQUAL_TO = LE


class LIKE(_RelationValue):
    _string_representation = 'LIKE'
    _allowed_types = six.string_types + (Query, CustomSql)


class REGEXP(_RelationValue):
    _string_representation = 'REGEXP'
    _allowed_types = six.string_types + (Query, CustomSql)


class IN(_RelationValue):
    _string_representation = 'IN'
    _allowed_types = (list, tuple, xrange, types.GeneratorType, Query, CustomSql)

    def __init__(self, *args):
        if len(args) > 1:
            value = args
        elif len(args) == 1:
            value = args[0]
        else:
            value = []
        try:
            #  Make list copy of value (if it is possible) because generators
            #+ give value only once.
            value = list(value)
        except TypeError:
            pass
        super(IN, self).__init__(value)


class IN_WITH_NONE(IN):
    _allowed_types = IN._allowed_types + (None,)

    def __init__(self, *args):
        if len(args) == 1 and args[0] is None:
            args = ([],)
        super(IN_WITH_NONE, self).__init__(*args)


class NOT_IN(IN):
    _string_representation = 'NOT IN'


class IS(_RelationValue):
    _string_representation = 'IS'
    _allowed_types = (bool, type(None), CustomSql)


class IS_NOT(IS):
    _string_representation = 'IS NOT'
