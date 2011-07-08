# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle._libs.argsParser
import sqlpuzzle._libs.sqlValue
import sqlpuzzle._features.conditions



INNER_JOIN = 0
LEFT_JOIN = 1
RIGHT_JOIN = 2

JOIN_TYPES = {
    INNER_JOIN: 'JOIN',
    LEFT_JOIN: 'LEFT JOIN',
    RIGHT_JOIN: 'RIGHT JOIN',
}



class OnCondition(sqlpuzzle._features.conditions.Condition):
    def __str__(self):
        """Print part of query."""
        return '%s = %s' % (
            sqlpuzzle._libs.sqlValue.SqlReference(self._column),
            sqlpuzzle._libs.sqlValue.SqlReference(self._value),
        )
    
    def __eq__(self, other):
        """Are on codntions equivalent?"""
        return (
            (self._column == other._column and self._value == other._value) or
            (self._column == other._value and self._value == other._column)
        )



class OnConditions(sqlpuzzle._features.conditions.Conditions):
    def __init__(self):
        """Initialization of OnConditions."""
        super(OnConditions, self).__init__(OnCondition)
        self._separatorOfFeatures = ' AND '



class Table(sqlpuzzle._features.Feature):
    def __init__(self, table=None, as_=None):
        """Initialization of Table."""
        self._table = table
        self._as = as_
        self._joins = []
    
    def __str__(self):
        """Print part of query."""
        if self._as:
            table = '%s AS %s' % (
                sqlpuzzle._libs.sqlValue.SqlReference(self._table),
                sqlpuzzle._libs.sqlValue.SqlReference(self._as),
            )
        else:
            table = str(sqlpuzzle._libs.sqlValue.SqlReference(self._table))
        
        if self._joins != []:
            if any([not join['ons'].isSet() for join in self._joins]):
                raise sqlpuzzle.exceptions.InvalidQueryException("You can't use join without on.")
            
            self.__minimizeJoins()
            table = '%s %s' % (
                table,
                ' '.join([
                    '%s %s ON (%s)' % (
                        JOIN_TYPES[join['type']],
                        str(join['table']),
                        str(join['ons']),
                    ) for join in self._joins
                ])
            )
        
        return table
    
    def __eq__(self, other):
        """Are tables equivalent?"""
        return (
            self._table == other._table and
            self._as == other._as and
            self._joins == other._joins
        )
    
    def __minimizeJoins(self):
        """
        Minimize of joins.
        Left/right and inner join of the same join is only inner join.
        """
        joinsGroup = []
        for join in self._joins:
            appendNew = True
            for joinGroup in joinsGroup:
                if joinGroup[0]['table'] == join['table'] and joinGroup[0]['ons'] == join['ons']:
                    joinGroup.append(join)
                    appendNew = False
                    break
            if appendNew:
                joinsGroup.append([join])
        
        self._joins = []
        for joins in joinsGroup:
            if len(joins) > 1 and any(bool(join['type'] == INNER_JOIN) for join in joins):
                joins[0]['type'] = INNER_JOIN
                self._joins.append(joins[0])
            else:
                self._joins.extend(joins)
        
    def isSimple(self):
        """Is set table without join?"""
        return self._joins == []
    
    def join(self, arg, joinType=INNER_JOIN):
        """Join table."""
        if isinstance(arg, (list, tuple)) and len(arg) == 2:
            table = Table(*arg)
        else:
            table = Table(arg)
        
        self._joins.append({
            'type': joinType,
            'table': table,
            'ons': OnConditions(),
        })
    
    def on(self, *args, **kwds):
        """Join on."""
        if self.isSimple():
            raise sqlpuzzle.exceptions.InvalidQueryException("You can't set join without table.")
        
        self._joins[-1]['ons'].where(*args, **kwds)



class Tables(sqlpuzzle._features.Features):
    def lastTable(self):
        """Get last table."""
        if self._features:
            return self._features[-1]
        raise sqlpuzzle.exceptions.SqlPuzzleException('Tables doesn\'t set - there is no last table.')
    
    def isSimple(self):
        """Is set only one table without join?"""
        return len(self._features) == 1 and self._features[0].isSimple()
    
    def set(self, *args):
        """Set tables."""
        args = [arg for arg in args if arg]
        
        allowedDataTypes = sqlpuzzle._libs.argsParser.AllowedDataTypes().add(
            (str, unicode, sqlpuzzle._queries.select.Select, sqlpuzzle._queries.union.Union),
            (str, unicode)
        ).add(
            sqlpuzzle.customSql.CustomSql
        )
        
        for table, as_ in sqlpuzzle._libs.argsParser.parseArgsToListOfTuples(
            {'maxItems': 2, 'allowedDataTypes': allowedDataTypes}, *args
        ):
            if self.isCustumSql(table):
                self.appendFeature(table)
            else:
                table = Table(table, as_)
                if table not in self:
                    self.appendFeature(table)
        
        return self
    
    def join(self, arg):
        """Join table."""
        return self.innerJoin(arg)
    
    def innerJoin(self, arg):
        """Inner join table."""
        if not self.isSet():
            raise sqlpuzzle.exceptions.InvalidQueryException("You can't set join without table.")
        
        self.lastTable().join(arg, INNER_JOIN)
        return self
    
    def leftJoin(self, arg):
        """Left join table."""
        if not self.isSet():
            raise sqlpuzzle.exceptions.InvalidQueryException("You can't set join without table.")
        
        self.lastTable().join(arg, LEFT_JOIN)
        return self
    
    def rightJoin(self, arg):
        """Right join table."""
        if not self.isSet():
            raise sqlpuzzle.exceptions.InvalidQueryException("You can't set join without table.")
        
        self.lastTable().join(arg, RIGHT_JOIN)
        return self
    
    def on(self, *args, **kwds):
        """Join on."""
        if not self.isSet():
            raise sqlpuzzle.exceptions.InvalidQueryException("You can't set condition of join without table.")
        
        self.lastTable().on(*args, **kwds)
        return self

