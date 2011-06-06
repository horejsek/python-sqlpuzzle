# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import datetime
import re


def addBackQuotes(value):
    """
    Add quotes.
    "table" => "`table`"
    "table.column" => "`table`.`column`"
    "table.col.umn" => "`table`.`col`.`umn`"
    "table.`col.umn`" => "`table`.`col.umn`"
    "`table`.`col.umn`" => "`table`.`col.umn`"
    """
    return '.'.join('`%s`' % i for i in re.split('`([^`]+)`|\.', value) if i)



class SqlValue:
    def __init__(self, value=None):
        """
        Initialization of Value.
        """
        self.value(value)
    
    def __str__(self):
        """
        Print part of query.
        """
        if isinstance(self.__value, (str, unicode)):
            return '"%s"' % self.__value
        elif isinstance(self.__value, (int, long)):
            return '%d' % self.__value
        elif isinstance(self.__value, float):
            return '%.5f' % self.__value
        elif isinstance(self.__value, (datetime.date, datetime.datetime)):
            return self.__value.isoformat()
        elif self.__value is None:
            return 'NULL'
        return 'undefined'
    
    def value(self, value):
        """
        Set value.
        """
        self.__value = value


