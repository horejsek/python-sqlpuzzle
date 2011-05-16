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
        self.__conditions = []
        self.__limit = None
        self.__offset = None
    
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
        return self
    
    def from_(self, *tables):
        """
        Set table(s) to query.
        """
        self.__tables = tables
        return self
    
    def where(self, *args, **kwargs):
        """
        Set condition(s) to query.
        """
        if len(args) == 1:
            if isinstance(args[0], (list, tuple)):
                try:
                    self.__conditions = [{
                        'column': condition[0],
                        'value': condition[1],
                        'relation': int(condition[2]),
                    } for condition in args[0]]
                except:
                    raise 'Conditions must have three items - column, value and relation.'
            elif isinstance(args[0], dict):
                self.__conditions = [{
                    'column': column,
                    'value': value,
                    'relation': EQUAL_TO,
                } for column, value in args[0].iteritems()]
        elif 2 <= len(args) <= 3:
            self.__conditions.append({
                'column': args[0],
                'value': args[1],
                'relation': EQUAL_TO if len(args) == 2 else int(args[2]),
            })
        elif kwargs is not None:
            self.__conditions = [{
                'column': column,
                'value': value,
                'relation': EQUAL_TO,
            } for column, value in kwargs.iteritems()]
        return self
    
    def limit(self, limit, offset=None):
        """
        Set limit (and offset).
        """
        if limit is None:
            self.__limit = None
            self.__offset = None
        else:
            self.__limit = int(limit)
        
        if offset is not None:
            self.offset(offset)
        return self
    
    def offset(self, offset):
        """
        Set offset.
        """
        self.__offset = int(offset)
        return self
    
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
        return self
    
    def insertInto(self, table):
        """
        Set query to insert.
        """
        return self.insert().into(table)
    
    def values(self, *args, **kwargs):
        """
        Set columns and values.
        """
        if len(args) == 1 and isinstance(args[0], dict):
            self.__columns = args[0].keys()
            self.__values = args[0].values()
        elif kwargs is not None:
            self.__columns = kwargs.keys()
            self.__values = kwargs.values()
        else:
            raise 'Values can be dictionary or keyworded variable arguments.'
        return self
    
    def update(self, table):
        """
        Set table for update.
        """
        self.__setSqlType(UPDATE)
        self.__tables = [table]
        return self
    
    def set(self, *args, **kwargs):
        """
        Set columns and values.
        """
        self.values(*args, **kwargs)
        return self
    
    def __str__(self):
        """
        Print query.
        """
        return self.getQuery()
    
    def getQuery(self):
        """
        Generate query.
        """
        if self.__sqlType == SELECT:
            return self.__generateSelect()
        elif self.__sqlType == INSERT:
            return self.__generateInsert()
        elif self.__sqlType == UPDATE:
            return self.__generateUpdate()
        raise 'Not implemented for sql type %s.' % self.__sqlType
    
    def __generateSelect(self):
        """
        Generate SELECT.
        """
        select = "SELECT %s FROM %s" % (
            ', '.join(('`%s`' % column for column in self.__columns)),
            ', '.join(('`%s`' % table for table in self.__tables)),
        )
        if self.__conditions:
            select = "%s WHERE %s" % (
                select,
                self.__generateWhere()
            )
        if self.__limit: select = "%s LIMIT %s" % (select, self.__limit)
        if self.__offset: select = "%s OFFSET %s" % (select, self.__offset)
        
        return select
    
    def __generateInsert(self):
        """
        Generate INSERT.
        """
        assert len(self.__tables) == 1, 'INSERT must have only one table.'
        assert not self.__conditions, 'INSERT does not have WHERE.'
        
        insert = "INSERT INTO `%s` (%s) VALUES (%s)" % (
            self.__tables[0],
            ', '.join(('`%s`' % column for column in self.__columns)),
            ', '.join(('"%s"' % value for value in self.__values)),
        )
        return insert
    
    def __generateUpdate(self):
        """
        Generate UPDATE.
        """
        assert len(self.__tables) == 1, 'INSERT must have only one table.'
        
        update = "UPDATE `%s` SET %s" % (
            self.__tables[0],
            ', '.join(('`%s` = "%s"' % (column, value) for column, value in zip(self.__columns, self.__values)))
        )
        if self.__conditions:
            update = "%s WHERE %s" % (
                update,
                self.__generateWhere()
            )
        
        return update

    def __generateWhere(self):
        """
        Generate WHERE.
        """
        where = ' AND '.join((
            '`%s` %s "%s"' % (
                condition['column'],
                RELATIONS[condition['relation']],
                condition['value']
            ) for condition in self.__conditions
        ))
        
        return where


