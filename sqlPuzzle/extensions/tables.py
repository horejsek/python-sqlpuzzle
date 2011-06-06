# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.argsParser
import sqlPuzzle.extensions.conditions
import sqlPuzzle.joinTypes
import sqlPuzzle.sqlValue



class On(sqlPuzzle.extensions.conditions.Condition):
    def __str__(self):
        """
        Print part of query.
        """
        return '%s %s %s' % (
            sqlPuzzle.sqlValue.addBackQuotes(self.getColumn()),
            sqlPuzzle.relations.RELATIONS[self.getRelation()],
            sqlPuzzle.sqlValue.addBackQuotes(self.getValue()),
        )



class Ons(sqlPuzzle.extensions.conditions.Conditions):
    _conditionObject = On
    
    def __str__(self):
        """
        Print part of query.
        """
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
        
        self.__joins = []
    
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
        
        if self.__joins != []:
            self.__minimizeJoins()
            table = '%s %s' % (
                table,
                ' '.join([
                    '%s %s ON (%s)' % (
                        sqlPuzzle.joinTypes.JOIN_TYPES[join['type']],
                        str(join['table']),
                        str(join['on'])
                    ) for join in self.__joins
                ])
            )
        
        return table
    
    def __minimizeJoins(self):
        """
        Minimize of joins.
        Left/right and inner join of the same join is only inner join.
        """
        joinsGroup = {}
        for join in self.__joins:
            joinStr = '%s %s' % (str(join['table']), str(join['on']))
            joinsGroup[joinStr] = joinsGroup.get(joinStr, [])
            joinsGroup[joinStr].append(join)
        
        self.__joins = []
        for joinStr, joins in joinsGroup.iteritems():
            if len(joins) > 1 and any(bool(join['type'] == sqlPuzzle.joinTypes.INNER_JOIN) for join in joins):
                joins[0]['type'] = sqlPuzzle.joinTypes.INNER_JOIN
                self.__joins.append(joins[0])
            else:
                self.__joins.extend(joins)
        
    def isSimple(self):
        """
        Is set table without join?
        """
        return self.__joins == []
    
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
            table = Table(*arg)
        else:
            table = Table(arg)
        
        self.__joins.append({
            'type': joinType,
            'table': table,
            'on': None,
        })
    
    def on(self, condition):
        """
        Join on.
        """
        self.__joins[-1]['on'] = condition


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
        args = [arg for arg in args if arg]
        
        for arg in sqlPuzzle.argsParser.parseArgsToListOfTuples({'maxItems': 2}, *args):
            table = Table(*arg)
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

