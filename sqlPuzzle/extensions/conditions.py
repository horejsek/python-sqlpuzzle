# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.argsParser
import sqlPuzzle.exceptions
import sqlPuzzle.sqlValue
import sqlPuzzle.relations


class Condition:
    def __init__(self):
        """
        Initialization of Condition.
        """
        self._column = None
        self._value = None
        self._relation = None
    
    def __str__(self):
        """
        Print condition (part of WHERE).
        """
        return '`%s` %s %s' % (
            self._column,
            sqlPuzzle.relations.RELATIONS[self._relation],
            sqlPuzzle.sqlValue.SqlValue(self._value),
        )
    
    def __eq__(self, other):
        return (
            self._column == other._column and
            self._value == other._value and
            self._relation == other._relation
        )
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def set(self, column, value, relation=None):
        """
        Set column, value and relation.
        """
        self.setColumn(column)
        self.setValue(value)
        self.setRelation(relation or sqlPuzzle.relations.EQ)
    
    def setColumn(self, column):
        """
        Set column.
        """
        self._column = column
    
    def setValue(self, value):
        """
        Set value.
        """
        self._value = value
    
    def setRelation(self, relation):
        """
        Set relation.
        """
        if relation not in sqlPuzzle.relations.RELATIONS:
            raise sqlPuzzle.exceptions.InvalidArgumentException()
        self._relation = relation


class Conditions:
    _conditionObject = Condition
    
    def __init__(self):
        """
        Initialization of Conditions.
        """
        self._conditions = []
    
    def __str__(self):
        """
        Print limit (part of query).
        """
        if self.isSet():
            return "WHERE %s" % " AND ".join(str(condition) for condition in self._conditions)
        return ""
    
    def __eq__(self, other):
        return all(bool(sc == oc) for sc, oc in zip(self._conditions, other._conditions))
    
    def __contains__(self, item):
        for condition in self._conditions:
            if item == condition:
                return True
        return False
    
    def isSet(self):
        """
        Is where set?
        """
        return self._conditions != []
    
    def where(self, *args, **kwds):
        """
        Set condition(s).
        """
        for column, value, relation in sqlPuzzle.argsParser.parseArgsToListOfTuples(
            {
                'minItems': 2,
                'maxItems': 3,
                'allowDict': True,
                'allowList': True,
                'allowedDataTypes': ((str, unicode), (str, unicode, int, long, float, bool), int),
            },
            *args,
            **kwds
        ):
            condition = self._conditionObject()
            condition.set(column, value, relation)
            if condition not in self:
                self._conditions.append(condition)
        
        return self
    
    def remove(self, *keys):
        """
        Remove condition(s).
        """
        if len(keys) == 0:
            self._conditions = []
        
        if not isinstance(keys, (list, tuple)):
            keys = (keys,)
        
        conditions = []
        for condition in self._conditions:
            if condition._column not in keys:
                conditions.append(condition)
        self._conditions = conditions


