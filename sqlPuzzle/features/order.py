# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.argsParser
import sqlPuzzle.sqlValue



ASC = 'ASC'
DESC = 'DESC'
ORDERING_TYPES = (ASC, DESC)



class Order(object):
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
        if self._sort == ASC:
            return str(sqlPuzzle.sqlValue.SqlReference(self._column))
        else:
            return '%s %s' % (
                sqlPuzzle.sqlValue.SqlReference(self._column),
                self._sort,
            )
    
    def __repr__(self):
        return "<Order: %s>" % self.__str__()
    
    def __eq__(self, other):
        """
        Are orders equivalent?
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
    
    def sort(self, sort=None):
        """
        Set type of sort (ASC or DESC).
        """
        if sort is None:
            sort = ASC
        
        sort = sort.upper()
        if sort in ORDERING_TYPES:
            self._sort = sort
        else:
            raise sqlPuzzle.exceptions.InvalidArgumentException('Type of order can be only %s.' % ' or '.join(ORDERING_TYPES))



class Orders(object):
    def __init__(self):
        """
        Initialization of OrderBy.
        """
        self._orders = []
    
    def __str__(self):
        """
        Print order (part of query).
        """
        raise sqlPuzzle.exceptions.SqlPuzzleNotImplemeted('Orders.__str__()')
    
    def __repr__(self):
        return "<Orders: %s>" % self.__str__()
    
    def __contains__(self, item):
        """
        Is item (order) in list of orders?
        """
        for order in self._orders:
            if item._column == order._column:
                return True
        return False
    
    def _changeSorting(self, columnName, sort):
        """
        If columnName in list, just set new sort.
        """
        for order in self._orders:
            if order._column == columnName:
                order.sort(sort)
    
    def isSet(self):
        """
        Is orderBy set?
        """
        return self._orders != []
    
    def order(self, *args):
        """
        Set Order.
        """
        for columnName, sort in sqlPuzzle.argsParser.parseArgsToListOfTuples(
            {'maxItems': 2, 'allowedDataTypes': (str, unicode)}, *args
        ):
            order = Order(columnName, sort)
            if order not in self:
                self._orders.append(order)
            else:
                self._changeSorting(columnName, sort)
        
        return self

