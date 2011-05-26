# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

class Column:
    def __init__(self, column=None, as_=None):
        """
        Initialization of Column.
        """
        self.column(column)
        self.as_(as_)
    
    def __str__(self):
        """
        Print part of query.
        """
        if self.__as:
            return '`%s` AS "%s"' % (
                self.__column,
                self.__as,
            )
        else:
            return '`%s`' % self.__column
    
    def column(self, column):
        """
        Set column.
        """
        self.__column = column
    
    def as_(self, as_):
        """
        Set as.
        """
        self.__as = as_


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
                    column.as_(arg[1])
            else:
                column.column(arg)
            self.__columns.append(column)
        
        return self

