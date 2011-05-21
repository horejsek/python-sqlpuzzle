# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

class Order:
    def __init__(self, column=None, sort='ASC'):
        self.column(column)
        self.sort(sort)
    
    def __str__(self):
        return '`%s` %s' % (
            self.__column,
            self.__sort,
        )
    
    def column(self, column):
        self.__column = column
    
    def sort(self, sort):
        sort = sort.upper()
        if sort in ('ASC', 'DESC'):
            self.__sort = sort
        else:
            self.__sort = 'ASC'


class OrderBy:
    def __init__(self):
        """
        Initialization of Order.
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
        Is order set?
        """
        return self.__orderBy != []
    
    def orderBy(self, *args):
        """
        Set ORDER BY.
        """
        for arg in args:
            order = Order()
            if isinstance(arg, (list, tuple)) and 1 <= len(arg) <= 2:
                order.column(arg[0])
                if len(arg) == 2:
                    order.sort(arg[1])
            else:
                order.column(arg)
            self.__orderBy.append(order)
        
        return self

