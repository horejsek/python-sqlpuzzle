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
        self.__tables = None
        self.__columns = None
        self.__values = None
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
    
    def insert(self):
        """
        Set query to insert.
        """
        self.__setSqlType(INSERT)
        return self
    
    def into(self, table):
        """
        Set table for insert.
        """
        self.__tables = [table]
    
    def values(self, *args, **kwargs):
        """
        Set values.
        """
        if len(args) == 1 and isinstance(args[0], dict):
            self.__columns = args[0].keys()
            self.__values = args[0].values()
        elif kwargs is not None:
            self.__columns = kwargs.keys()
            self.__values = kwargs.values()
        else:
            raise 'Values can be dictionary or keyworded variable arguments.'
    
    def getQuery(self):
        """
        Generate query.
        """
        if self.__sqlType == SELECT:
            return self.__generateSelect()
        elif self.__sqlType == INSERT:
            return self.__generateInsert()
        raise 'Not implemented for sql type %s.' % self.__sqlType
    
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
    
    def __generateInsert(self):
        """
        Generate INSERT.
        """
        assert len(self.__tables) == 1, 'INSERT must have only one table.'
        assert self.__conditions is None, 'INSERT does not have WHERE.'
        
        insert = "INSERT INTO `%s` (%s) VALUES (%s)" % (
            self.__tables[0],
            ', '.join(('`%s`' % column for column in self.__columns)),
            ', '.join(('"%s"' % value for value in self.__values)),
        )
        return insert

    def __generateWhere(self):
        """
        Generate WHERE.
        """
        where = ' AND '.join(('`%s` %s "%s"' % (column, RELATIONS[relation], value) for column, value, relation in self.__conditions))
        return where


