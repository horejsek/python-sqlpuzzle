# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import types
import datetime

import sqlpuzzle._libs.object
import sqlpuzzle.exceptions



class _RelationValue(sqlpuzzle._libs.object.Object):
    _stringRepresntation = 'Abstract Relation'
    _allowedTypes = ()

    def __init__(self, value):
        self._checkValueType(value)
        self._value = value

    def __str__(self):
        return self._stringRepresntation

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
    _allowedTypes = (str, unicode, int, long, float, bool)
EQUAL_TO = EQ



class NE(EQ):
    _stringRepresntation = '!='
NOT_EQUAL_TO = NE



class GT(_RelationValue):
    _stringRepresntation = '>'
    _allowedTypes = (int, long, float, datetime.date, datetime.datetime)
GRATHER_THAN = GT



class GE(GT):
    _stringRepresntation = '>='
GRATHER_THAN_OR_EQUAL_TO = GE



class LT(GT):
    _stringRepresntation = '<'
LESS_THAN = LT



class LE(GT):
    _stringRepresntation = '<='
LESS_TAHN_OR_EQUAL_TO = LE



class LIKE(_RelationValue):
    _stringRepresntation = 'LIKE'
    _allowedTypes = (str, unicode)



class REGEXP(_RelationValue):
    _stringRepresntation = 'REGEXP'
    _allowedTypes = (str, unicode)



class IN(_RelationValue):
    _stringRepresntation = 'IN'
    _allowedTypes = (list, tuple)

    def __init__(self, *args):
        if len(args) > 1:
            value = args
        else:
            value = args[0]
        super(IN, self).__init__(value)



class NOT_IN(IN):
    _stringRepresntation = 'NOT IN'



class IS(_RelationValue):
    _stringRepresntation = 'IS'
    _allowedTypes = (types.NoneType,)



class IS_NOT(IS):
    _stringRepresntation = 'IS NOT'
