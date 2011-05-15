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


SELECT = 1
INSERT = 2
UPDATE = 3


class SqlPuzzle:
    def __init__(self):
        """
        Initialization of SqlPuzzle.
        """
        self.__sqlType = None
        self.__columns = None
        self.__tables = None
        self.__conditions = None
    
    def __setSqlType(self, type_):
        assert type_ is not None, 'You can\'t change type of query.'
        assert type_ in (SELECT, INSERT, UPDATE), 'Type \'%s\' of query is undefind.' % type_
        self.__sqlType = type_
    
    def select(self, *columns):
        """
        Set column(s) to select.
        """
        self.__setSqlType(SELECT)
        self.__columns = columns
    
    def from_(self, *tables):
        """
        Set table(s) to query.
        """
        self.__tables = tables
    
    def where(self, *conditions):
        """
        Set condition(s) to query.
        """
        if isinstance(conditions[0], (list, tuple)):
            self.__conditions = conditions
        elif isinstance(conditions[0], str) and len(conditions) == 3:
            try: self.__conditions.append(tuple(conditions))
            except: self.__conditions = [tuple(conditions)]
    
    def getQuery(self):
        """
        Generate query.
        """
        if self.__sqlType == SELECT:
            return self.__generateSelect()
    
    def __generateSelect(self):
        """
        Generate SELECT.
        """
        select = "SELECT %s FROM %s" % (
            ', '.join(('`%s`' % column for column in self.__columns)),
            ', '.join(('`%s`' % table for table in self.__tables)),
        )
        if self.__conditions is not None:
            select = "%s WHERE %s" % (
                select,
                self.__generateWhere()
            )
        
        return select

    def __generateWhere(self):
        """
        Generate WHERE.
        """
        where = ' AND '.join(('`%s` %s "%s"' % (column, RELATIONS[relation], value) for column, value, relation in self.__conditions))
        return where


