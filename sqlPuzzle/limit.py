# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

class Limit:
    def __init__(self):
        """
        Initialization of Limit.
        """
        self.__limit = None
        self.__offset = None
    
    def __str__(self):
        """
        Print limit (part of query).
        """
        limit = "LIMIT %s" % self.__limit
        if self.__offset is not None:
            limit = "%s OFFSET %s" % (limit, self.__offset)
        return limit
    
    def isSet(self):
        """
        Is limit set?
        """
        return self.__limit is not None
    
    def limit(self, limit, offset=None):
        """
        Set LIMIT (and OFFSET).
        """
        if limit is None:
            self.__limit = None
            self.__offset = None
        else:
            self.__limit = int(limit)
        
        if offset is not None:
            self.offset(offset)
        
        return self
    
    def offset(self, offset):
        """
        Set OFFSET.
        """
        self.__offset = int(offset)
        return self

