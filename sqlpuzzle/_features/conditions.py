# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

import types
import datetime

import sqlpuzzle._libs.argsParser
import sqlpuzzle._libs.sqlValue
import sqlpuzzle._queries
import sqlpuzzle.exceptions
import sqlpuzzle.relations


class Condition(sqlpuzzle._features.Feature):
    _defaultRelations = {
        str: sqlpuzzle.relations.EQ,
        unicode: sqlpuzzle.relations.EQ,
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
        self._column = column
        self._setRelationValue(value, relation)

    def _setRelationValue(self, value, relation):
        if isinstance(relation, type) and issubclass(relation, sqlpuzzle.relations._RelationValue):
            relationValue = relation(value)
        elif not isinstance(value, sqlpuzzle.relations._RelationValue):
            relationValue = self._createDefaultRelationValue(value)
        else:
            relationValue = value
        self._relationValue = relationValue

    def _createDefaultRelationValue(self, value):
        return self._defaultRelations[type(value)](value)

    def __str__(self):
        """Print condition (part of WHERE)."""
        foo = '%(col)s %(rel)s %(val)s'
        value = self._value
        if isinstance(value, (list, tuple, xrange)) and None in value:
            foo = '(' + foo + ' OR %(col)s IS NULL)'
            value = filter(lambda x: x is not None, value)
        return foo % {
            'col': sqlpuzzle._libs.sqlValue.SqlReference(self._column),
            'rel': self._relation,
            'val': sqlpuzzle._libs.sqlValue.SqlValue(value),
        }

    def __eq__(self, other):
        """Are conditions equivalent?"""
        return (
            self._column == other._column and
            self._relationValue == other._relationValue
        )

    @property
    def _value(self):
        return self._relationValue.getValue()

    @property
    def _relation(self):
        return self._relationValue.getRelation()



class Conditions(sqlpuzzle._features.Features):
    def __init__(self, conditionObject=Condition):
        """Initialization of Conditions."""
        super(Conditions, self).__init__()
        self._conditionObject = conditionObject

    def where(self, *args, **kwds):
        """Set condition(s)."""
        if args and self.isCustumSql(args[0]):
            self.appendFeature(args[0])

        else:
            for column, value, relation in sqlpuzzle._libs.argsParser.parseArgsToListOfTuples(
                {
                    'minItems': 2,
                    'maxItems': 3, # TODO: In version 1.0 third param will be removed.
                    'allowDict': True,
                    'allowList': True,
                    'allowedDataTypes': (
                        (str, unicode, sqlpuzzle._queries.select.Select),
                        (str, unicode, int, long, float, bool, list, tuple, xrange, types.GeneratorType, datetime.date, datetime.datetime, sqlpuzzle.relations._RelationValue, sqlpuzzle._queries.select.Select),
                        (sqlpuzzle.relations._RelationValue,)
                    ),
                },
                *args,
                **kwds
            ):
                # TODO: Remove in version 1.0.
                if relation is not None:
                    print 'Third param in condition (relation) is deprecated. Instead use relation as instance with value - e.g. sqlpuzzle.relation.LIKE("Harry").'

                condition = self._conditionObject(column, value, relation)
                if condition not in self:
                    self.appendFeature(condition)

        return self
