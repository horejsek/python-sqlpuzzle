# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlValue


class Values:
    def __init__(self):
        """
        Initialization of Values.
        """
        self.__values = {}
    
    def __str__(self):
        """
        Print values (part of query).
        """
        return ', '.join('`%s` = %s' % (column, str(sqlValue.SqlValue(value))) for column, value in self.__values.iteritems())
    
    def columns(self):
        """
        Print columns of values.
        """
        return ', '.join('`%s`' % column for column in self.__values.keys())
    
    def values(self):
        """
        Print values of values.
        """
        return ', '.join('%s' % str(sqlValue.SqlValue(value)) for value in self.__values.values())
    
    def isSet(self):
        """
        Is limit set?
        """
        return self.__values != {}
    
    def set(self, *args, **kwds):
        """
        Set columns.
        """
        list_ = None
        dict_ = None
        
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            list_ = args[0]
        elif len(args) == 1 and isinstance(args[0], dict):
            dict_ = args[0]
        elif len(args) == 2:
            list_ = (args,)
        elif kwds is not None:
            dict_ = kwds
        
        if list_ is not None:
            self.__values.update(dict(list_))
        elif dict_ is not None:
            self.__values.update(dict_)
        
        return self

