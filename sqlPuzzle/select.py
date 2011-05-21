# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import query


class Select(query.Query):
    def __init__(self, *columns):
        """
        Initialization of Select.
        """
        query.Query.__init__(self)
        self._columns = columns
    
    def __str__(self):
        """
        Print query.
        """
        select = "SELECT %s FROM %s" % (
            ', '.join(('`%s`' % column for column in self._columns)),
            str(self._tables),
        )
        if self._conditions.isSet(): select = "%s %s" % (select, self._conditions)
        if self._limit.isSet(): select = "%s %s" % (select, self._limit)
        
        return select
    
    def _typeOfQuery(self):
        return 'SELECT'
    
    def from_(self, *tables):
        """
        Set table(s) to query.
        """
        self._tables.set(tables)
        return self
    
    def where(self, *args, **kwargs):
        """
        Set condition(s) to query.
        """
        self._conditions.where(*args, **kwargs)
        return self
    
    def limit(self, limit, offset=None):
        """
        Set limit (and offset).
        """
        self._limit.limit(limit, offset)
        return self
    
    def offset(self, offset):
        """
        Set offset.
        """
        self._limit.offset(offset)
        return self

