# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle._libs.argsParser
import sqlpuzzle._libs.sqlValue



ASC = 'ASC'
DESC = 'DESC'
ORDERING_TYPES = (ASC, DESC)



class Order(sqlpuzzle._features.Feature):
    def __init__(self, column=None, sort=None):
        """Initialization of Order."""
        self.column(column)
        self.sort(sort)
    
    def __str__(self):
        """Print part of query."""
        if self._sort == ASC:
            return str(sqlpuzzle._libs.sqlValue.SqlReference(self._column))
        else:
            return '%s %s' % (
                sqlpuzzle._libs.sqlValue.SqlReference(self._column),
                self._sort,
            )
    
    def __eq__(self, other):
        """Are orders equivalent?"""
        return (
            self._column == other._column and
            self._sort == other._sort
        )
    
    def column(self, column):
        """Set column."""
        self._column = column
    
    def sort(self, sort=None):
        """Set type of sort (ASC or DESC)."""
        if sort is None:
            sort = ASC
        
        sort = sort.upper()
        if sort in ORDERING_TYPES:
            self._sort = sort
        else:
            raise sqlpuzzle.exceptions.InvalidArgumentException('Type of order can be only %s.' % ' or '.join(ORDERING_TYPES))



class Orders(sqlpuzzle._features.Features):
    def __contains__(self, item):
        """Is item (order) in list of orders?"""
        for order in self._features:
            if item._column == order._column:
                return True
        return False
    
    def _changeSorting(self, columnName, sort):
        """If columnName in list, just set new sort."""
        for order in self._features:
            if order._column == columnName:
                order.sort(sort)
    
    def order(self, *args):
        """Set Order."""
        for columnName, sort in sqlpuzzle._libs.argsParser.parseArgsToListOfTuples(
            {'maxItems': 2, 'allowedDataTypes': (str, unicode, int)}, *args
        ):
            order = Order(columnName, sort)
            if order not in self:
                self._features.append(order)
            else:
                self._changeSorting(columnName, sort)
        
        return self

