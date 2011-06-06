# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.argsParser
import sqlPuzzle.extensions.orderBy


class Group(sqlPuzzle.extensions.orderBy.Order):
    pass


class GroupBy:
    def __init__(self):
        """
        Initialization of GroupBy.
        """
        self._groupBy = []
    
    def __str__(self):
        """
        Print order (part of query).
        """
        groupBy = "GROUP BY %s" % ', '.join(str(group) for group in self._groupBy)
        return groupBy
    
    def __contains__(self, item):
        for group in self._groupBy:
            if item._column == group._column:
                return True
        return False
    
    def __changeSorting(self, columnName, sort):
        for group in self._groupBy:
            if group._column == columnName:
                group.sort(sort)
    
    def isSet(self):
        """
        Is groupBy set?
        """
        return self._groupBy != []
    
    def groupBy(self, *args):
        """
        Set GROUP BY.
        """
        for columnName, sort in sqlPuzzle.argsParser.parseArgsToListOfTuples(
            {'maxItems': 2, 'allowedDataTypes': (str, unicode)}, *args
        ):
            group = Group(columnName, sort)
            if group not in self:
                self._groupBy.append(group)
            else:
                self.__changeSorting(columnName, sort)
        
        return self

