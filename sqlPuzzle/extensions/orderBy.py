# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.argsParser
import sqlPuzzle.sqlValue


class Order:
    def __init__(self, column=None, sort=None):
        """
        Initialization of Order.
        """
        self.column(column)
        self.sort(sort)
    
    def __str__(self):
        """
        Print part of query.
        """
        if self._sort == 'ASC':
            return sqlPuzzle.sqlValue.addBackQuotes(self._column)
        else:
            return '%s %s' % (
                sqlPuzzle.sqlValue.addBackQuotes(self._column),
                self._sort,
            )
    
    def __eq__(self, other):
        """
        Is orders equivalent?
        """
        return (
            self._column == other._column and
            self._sort == other._sort
        )
    
    def column(self, column):
        """
        Set column.
        """
        self._column = column
    
    def sort(self, sort):
        """
        Set type of sort (ASC or DESC).
        """
        if sort is None:
            sort = 'ASC'
        
        sort = sort.upper()
        if sort in ('ASC', 'DESC'):
            self._sort = sort
        else:
            raise sqlPuzzle.exceptions.InvalidArgumentException('Type of order can be only ASC or DESC.')


class OrderBy:
    def __init__(self):
        """
        Initialization of OrderBy.
        """
        self._orderBy = []
    
    def __str__(self):
        """
        Print order (part of query).
        """
        orderBy = "ORDER BY %s" % ', '.join(str(order) for order in self._orderBy)
        return orderBy
    
    def __contains__(self, item):
        for order in self._orderBy:
            if item._column == order._column:
                return True
        return False
    
    def __changeSorting(self, columnName, sort):
        for order in self._orderBy:
            if order._column == columnName:
                order.sort(sort)
    
    def isSet(self):
        """
        Is orderBy set?
        """
        return self._orderBy != []
    
    def orderBy(self, *args):
        """
        Set ORDER BY.
        """
        for columnName, sort in sqlPuzzle.argsParser.parseArgsToListOfTuples(
            {'maxItems': 2, 'allowedDataTypes': (str, unicode)}, *args
        ):
            order = Order(columnName, sort)
            if order not in self:
                self._orderBy.append(order)
            else:
                self.__changeSorting(columnName, sort)
        
        return self

