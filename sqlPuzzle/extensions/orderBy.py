# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.argsParser


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
        if self.__sort == 'ASC':
            return '`%s`' % self.__column
        else:
            return '`%s` %s' % (
                self.__column,
                self.__sort,
            )
    
    def column(self, column):
        """
        Set column.
        """
        self.__column = column
    
    def sort(self, sort):
        """
        Set type of sort (ASC or DESC).
        """
        if sort is None:
            sort = 'ASC'
        
        sort = sort.upper()
        if sort in ('ASC', 'DESC'):
            self.__sort = sort
        else:
            self.__sort = 'ASC'


class OrderBy:
    def __init__(self):
        """
        Initialization of OrderBy.
        """
        self.__orderBy = []
    
    def __str__(self):
        """
        Print order (part of query).
        """
        orderBy = "ORDER BY %s" % ', '.join(str(order) for order in self.__orderBy)
        return orderBy
    
    def isSet(self):
        """
        Is orderBy set?
        """
        return self.__orderBy != []
    
    def orderBy(self, *args):
        """
        Set ORDER BY.
        """
        for arg in sqlPuzzle.argsParser.parseArgsToListOfTuples({'maxItems': 2}, *args):
            order = Order(*arg)
            self.__orderBy.append(order)
        
        return self

