# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.extensions.conditions
import sqlPuzzle.joinTypes


class On(sqlPuzzle.extensions.conditions.Condition):
    def __str__(self):
        return '`%s` %s `%s`' % (
            self.getColumn().replace('.', '`.`', 1),
            sqlPuzzle.relations.RELATIONS[self.getRelation()],
            self.getValue().replace('.', '`.`', 1),
        )



class Ons(sqlPuzzle.extensions.conditions.Conditions):
    _conditionObject = On
    
    def __str__(self):
        if self.isSet():
            return " AND ".join(str(condition) for condition in self._getConditions())
        return ""



class Table:
    def __init__(self, table=None, as_=None):
        """
        Initialization of Table.
        """
        self.table(table)
        self.as_(as_)
        
        self.__join = []
    
    def __str__(self):
        """
        Print part of query.
        """
        if self.__as:
            table = '`%s` AS `%s`' % (
                self.__table,
                self.__as,
            )
        else:
            table = '`%s`' % self.__table
        
        if self.__join != []:
            table = '%s %s' % (
                table,
                ' '.join([
                    '%s %s ON (%s)' % (
                        sqlPuzzle.joinTypes.JOIN_TYPES[join['type']],
                        str(join['table']),
                        str(join['on'])
                    ) for join in self.__join
                ])
            )
        
        return table
    
    def isSimple(self):
        """
        Is set table without join?
        """
        return self.__join == []
    
    def table(self, table):
        """
        Set table.
        """
        self.__table = table
    
    def as_(self, as_):
        """
        Set as.
        """
        self.__as = as_
    
    def join(self, arg, joinType=sqlPuzzle.joinTypes.INNER_JOIN):
        """
        Join table.
        """
        if isinstance(arg, (list, tuple)) and len(arg) == 2:
            table = arg[0]
            as_ = arg[1]
        else:
            table = arg
            as_ = None
        
        self.__join.append({
            'type': joinType,
            'table': Table(table, as_),
            'on': None,
        })
    
    def on(self, condition):
        """
        Join on.
        """
        self.__join[-1]['on'] = condition


class Tables:
    def __init__(self):
        """
        Initialization of Tables.
        """
        self.__tables = []
    
    def __str__(self):
        """
        Print tables (part of query).
        """
        return ", ".join(str(table) for table in self.__tables)
    
    def isSet(self):
        """
        Is tables set?
        """
        return self.__tables != []
    
    def isSimple(self):
        """
        Is set only one table without join?
        """
        return len(self.__tables) == 1 and self.__tables[0].isSimple()
    
    def set(self, *args):
        """
        Set tables.
        """
        for arg in args:
            if arg is None:
                continue
            
            table = Table()
            if isinstance(arg, (list, tuple)) and 1 <= len(arg) <= 2:
                table.table(arg[0])
                if len(arg) == 2:
                    table.as_(arg[1])
            else:
                table.table(arg)
            self.__tables.append(table)
        
        return self
    
    def join(self, arg):
        """
        Join table.
        """
        self.__tables[-1].join(arg, sqlPuzzle.joinTypes.INNER_JOIN)
        return self
    
    def innerJoin(self, arg):
        """
        Inner join table.
        """
        self.__tables[-1].join(arg, sqlPuzzle.joinTypes.INNER_JOIN)
        return self
    
    def leftJoin(self, arg):
        """
        Left join table.
        """
        self.__tables[-1].join(arg, sqlPuzzle.joinTypes.LEFT_JOIN)
        return self
    
    def rightJoin(self, arg):
        """
        Right join table.
        """
        self.__tables[-1].join(arg, sqlPuzzle.joinTypes.RIGHT_JOIN)
        return self
    
    def on(self, *args, **kwds):
        """
        Join on.
        """
        condition = Ons()
        condition.where(*args, **kwds)
        
        self.__tables[-1].on(condition)
        return self

