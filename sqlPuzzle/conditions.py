# -*- coding: utf-8 -*-


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
        return '`%s` %s "%s"' % (
            self.__column,
            RELATIONS[self.__relation],
            self.__value,
        )
    
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
        return "WHERE %s" % " AND ".join(str(condition) for condition in self.__conditions)
    
    def isSet(self):
        """
        Is where set?
        """
        return True if self.__conditions else False
    
    def where(self, *args, **kwargs):
        """
        Set condition(s).
        """
        if len(args) == 1:
            if isinstance(args[0], (list, tuple)):
                for condition in args[0]:
                    c = Condition()
                    c.set(condition[0], condition[1])
                    if len(condition) == 3: c.setRelation(condition[2])
                    self.__conditions.append(c)
            elif isinstance(args[0], dict):
                for column, value in args[0].iteritems():
                    c = Condition()
                    c.set(column, value)
                    self.__conditions.append(c)
        elif 2 <= len(args) <= 3:
            c = Condition()
            c.set(args[0], args[1])
            if len(args) == 3: c.setRelation(args[2])
            self.__conditions.append(c)
        elif kwargs is not None:
            for column, value in kwargs.iteritems():
                c = Condition()
                c.set(column, value)
                self.__conditions.append(c)


