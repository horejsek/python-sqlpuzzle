# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

class Value:
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
        elif isinstance(self.__value, (int, long, float)):
            return '%d' % self.__value
        elif self.__value is None:
            return 'NULL'
        return 'undefined'
    
    def value(self, value):
        """
        Set value.
        """
        self.__value = value


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
        return ', '.join('`%s` = %s' % (column, str(Value(value))) for column, value in self.__values.iteritems())
    
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

