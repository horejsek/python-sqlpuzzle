# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

EQ = EQUAL_TO = 1
NE = NOT_EQUAL_TO = 2

GT = GRATHER_THAN = 3
GE = GRATHER_THAN_OR_EQUAL_TO = 4

LT = LESS_THAN = 5
LE = LESS_TAHN_OR_EQUAL_TO = 6

LIKE = 7


RELATIONS = {
    EQ: '=',
    NE: '!=',
    GT: '>',
    GE: '>=',
    LT: '<',
    LE: '<=',
    LIKE: 'LIKE',
}


class Condition:
    def __init__(self):
        """
        Initialization of Condition.
        """
        self.__column = None
        self.__value = None
        self.__relation = None
    
    def __str__(self):
        """
        Print condition (part of WHERE).
        """
        if isinstance(self.__value, int):
            formatString = '`%s` %s %s'
        else:
            formatString = '`%s` %s "%s"'
            
        return formatString % (
            self.__column,
            RELATIONS[self.__relation],
            self.__value,
        )
    
    def __eq__(self, other):
        return (
            self.getColumn() == other.getColumn() and
            self.getValue() == other.getValue() and
            self.getRelation() == other.getRelation()
        )
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def set(self, column, value, relation=None):
        """
        Set column, value and relation.
        """
        self.setColumn(column)
        self.setValue(value)
        self.setRelation(relation or EQ)
    
    def setColumn(self, column):
        """
        Set column.
        """
        self.__column = column
    
    def setValue(self, value):
        """
        Set value.
        """
        self.__value = value
    
    def setRelation(self, relation):
        """
        Set relation.
        """
        self.__relation = relation
    
    def getColumn(self):
        """
        Get column.
        """
        return self.__column
    
    def getValue(self):
        """
        Get value.
        """
        return self.__value
    
    def getRelation(self):
        """
        Get relation.
        """
        return self.__relation


class Conditions:
    def __init__(self):
        """
        Initialization of Conditions.
        """
        self.__conditions = []
    
    def __str__(self):
        """
        Print limit (part of query).
        """
        if self.isSet():
            return "WHERE %s" % " AND ".join(str(condition) for condition in self.__conditions)
        return ""
    
    def isSet(self):
        """
        Is where set?
        """
        return self.__conditions != []
    
    def where(self, *args, **kwds):
        """
        Set condition(s).
        """
        list_ = None
        dict_ = None
        
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            list_ = args[0]
        elif len(args) == 1 and isinstance(args[0], dict):
            dict_ = args[0]
        elif 2 <= len(args) <= 3:
            list_ = (args,)
        elif kwds is not None:
            dict_ = kwds
        
        if list_ is not None:
            for c in list_:
                condition = Condition()
                condition.set(c[0], c[1])
                if len(c) == 3:
                    condition.setRelation(c[2])
                self.__conditions.append(condition)
        elif dict_ is not None:
            for c, v in dict_.iteritems():
                condition = Condition()
                condition.set(c, v)
                self.__conditions.append(condition)
    
    def remove(self, *keys):
        """
        Remove condition(s).
        """
        if len(keys) == 0:
            self.__conditions = []
        
        if not isinstance(keys, (list, tuple)):
            keys = (keys,)
        
        conditions = []
        for condition in self.__conditions:
            if condition.getColumn() not in keys:
                conditions.append(condition)
        self.__conditions = conditions

