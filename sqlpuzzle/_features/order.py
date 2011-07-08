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
        self._column = column
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
    def _findOrderByName(self, columnName):
        """Find Order instance by column name."""
        for order in self._features:
            if order._column == columnName:
                return order
        return None
    
    def order(self, *args):
        """Set Order."""
        for columnName, sort in sqlpuzzle._libs.argsParser.parseArgsToListOfTuples(
            {'maxItems': 2, 'allowedDataTypes': (str, unicode, int)}, *args
        ):
            order = self._findOrderByName(columnName)
            if order is None:
                order = Order(columnName, sort)
                self.appendFeature(order)
            else:
                order.sort(sort)
        
        return self

