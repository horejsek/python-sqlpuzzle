# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import datetime


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


