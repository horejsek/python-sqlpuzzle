# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

import types
import datetime

import sqlpuzzle._libs.object
from sqlpuzzle._libs.customSql import CustomSql
from sqlpuzzle._queries import Query



class _RelationValue(sqlpuzzle._libs.object.Object):
    _stringRepresntation = 'Abstract Relation'
    _allowedTypes = ()

    def __init__(self, value):
        self._checkValueType(value)
        self._value = value

    def __str__(self):
        return '"%s %s"' % (
            self._stringRepresntation,
            self._value,
        )

    def __eq__(self, other):
        """Are relations equivalent?"""
        return (
            self.__class__ == other.__class__ and
            self._value == other._value
        )

    def _checkValueType(self, value):
        # isinstance(True, (int, long)) is True => must be special condition
        if (
            (bool not in self._allowedTypes and isinstance(value, types.BooleanType)) or
            not isinstance(value, self._allowedTypes)
        ):
            raise sqlpuzzle.exceptions.InvalidArgumentException(
                'Relation "%s" is not allowed for data type "%s".' % (
                    self._stringRepresntation,
                    type(value)
                )
            )

    def getRelation(self):
        return self._stringRepresntation

    def getValue(self):
        return self._value



class EQ(_RelationValue):
    _stringRepresntation = '='
    _allowedTypes = (str, unicode, int, long, float, bool, datetime.date, Query, CustomSql)
EQUAL_TO = EQ



class NE(EQ):
    _stringRepresntation = '!='
NOT_EQUAL_TO = NE



class GT(_RelationValue):
    _stringRepresntation = '>'
    _allowedTypes = (int, long, float, datetime.date, Query, CustomSql)
GRATHER_THAN = GT



class GE(GT):
    _stringRepresntation = '>='
GRATHER_THAN_OR_EQUAL_TO = GE



class LT(GT):
    _stringRepresntation = '<'
LESS_THAN = LT



class LE(GT):
    _stringRepresntation = '<='
LESS_THAN_OR_EQUAL_TO = LE



class LIKE(_RelationValue):
    _stringRepresntation = 'LIKE'
    _allowedTypes = (str, unicode, Query, CustomSql)



class REGEXP(_RelationValue):
    _stringRepresntation = 'REGEXP'
    _allowedTypes = (str, unicode, Query, CustomSql)



class IN(_RelationValue):
    _stringRepresntation = 'IN'
    _allowedTypes = (list, tuple, xrange, types.GeneratorType, Query, CustomSql)

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
    _allowedTypes = IN._allowedTypes + (None,)

    def __init__(self, *args):
        if len(args) == 1 and args[0] is None:
            args = ([],)
        super(IN_WITH_NONE, self).__init__(*args)



class NOT_IN(IN):
    _stringRepresntation = 'NOT IN'



class IS(_RelationValue):
    _stringRepresntation = 'IS'
    _allowedTypes = (bool, types.NoneType, CustomSql)



class IS_NOT(IS):
    _stringRepresntation = 'IS NOT'

