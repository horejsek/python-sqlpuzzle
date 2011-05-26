# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.extensions.orderBy


class Group(sqlPuzzle.extensions.orderBy.Order):
    pass


class GroupBy:
    def __init__(self):
        """
        Initialization of GroupBy.
        """
        self.__groupBy = []
    
    def __str__(self):
        """
        Print order (part of query).
        """
        groupBy = "GROUP BY %s" % ', '.join(str(group) for group in self.__groupBy)
        return groupBy
    
    def isSet(self):
        """
        Is groupBy set?
        """
        return self.__groupBy != []
    
    def groupBy(self, *args):
        """
        Set GROUP BY.
        """
        for arg in args:
            group = Group()
            if isinstance(arg, (list, tuple)) and 1 <= len(arg) <= 2:
                group.column(arg[0])
                if len(arg) == 2:
                    group.sort(arg[1])
            else:
                group.column(arg)
            self.__groupBy.append(group)
        
        return self

