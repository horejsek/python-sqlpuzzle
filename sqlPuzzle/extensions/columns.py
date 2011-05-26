# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

class Column:
    def __init__(self, column=None, columnAs=None):
        """
        Initialization of Column.
        """
        self.column(column)
        self.columnAs(columnAs)
    
    def __str__(self):
        """
        Print part of query.
        """
        if self.__columnAs:
            return '`%s` AS "%s"' % (
                self.__column,
                self.__columnAs,
            )
        else:
            return '`%s`' % self.__column
    
    def column(self, column):
        """
        Set column.
        """
        self.__column = column
    
    def columnAs(self, columnAs):
        """
        Set as.
        """
        self.__columnAs = columnAs


class Columns:
    def __init__(self):
        """
        Initialization of Columns.
        """
        self.__columns = []
    
    def __str__(self):
        """
        Print columns (part of query).
        """
        if self.isSet():
            return ', '.join(str(column) for column in self.__columns)
        else:
            return '*'
    
    def isSet(self):
        """
        Is limit set?
        """
        return self.__columns != []
    
    def columns(self, *args):
        """
        Set columns.
        """
        for arg in args:
            column = Column()
            if isinstance(arg, (list, tuple)) and 1 <= len(arg) <= 2:
                column.column(arg[0])
                if len(arg) == 2:
                    column.columnAs(arg[1])
            else:
                column.column(arg)
            self.__columns.append(column)
        
        return self

