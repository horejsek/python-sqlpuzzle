# -*- coding: utf-8 -*-

import types
import datetime

import sqlpuzzle._libs.object
import sqlpuzzle._queries
import sqlpuzzle.exceptions


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
    _allowed_types = (str, unicode, int, long, float,
                     bool, datetime.date, sqlpuzzle._queries.Query)
EQUAL_TO = EQ


class NE(EQ):
    _string_representation = '!='
NOT_EQUAL_TO = NE


class GT(_RelationValue):
    _string_representation = '>'
    _allowed_types = (int, long, float, datetime.date, sqlpuzzle._queries.Query)
GRATHER_THAN = GT


class GE(GT):
    _string_representation = '>='
GRATHER_THAN_OR_EQUAL_TO = GE


class LT(GT):
    _string_representation = '<'
LESS_THAN = LT


class LE(GT):
    _string_representation = '<='
LESS_TAHN_OR_EQUAL_TO = LE


class LIKE(_RelationValue):
    _string_representation = 'LIKE'
    _allowed_types = (str, unicode, sqlpuzzle._queries.Query)


class REGEXP(_RelationValue):
    _string_representation = 'REGEXP'
    _allowed_types = (str, unicode, sqlpuzzle._queries.Query)


class IN(_RelationValue):
    _string_representation = 'IN'
    _allowed_types = (list, tuple, xrange, types.GeneratorType, sqlpuzzle._queries.Query)

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
    _allowed_types = (bool, type(None),)


class IS_NOT(IS):
    _string_representation = 'IS NOT'
