# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import query


class Insert(query.Query):
    def __init__(self):
        """
        Initialization of Insert.
        """
        query.Query.__init__(self)
        self._columns = None
        self._values = None
    
    def __str__(self):
        """
        Print query.
        """
        insert = "INSERT INTO %s (%s) VALUES (%s)" % (
            str(self._tables),
            ', '.join(('`%s`' % column for column in self._columns)),
            ', '.join(('"%s"' % value for value in self._values)),
        )
        return insert
    
    def _typeOfQuery(self):
        return 'INSERT'
    
    def into(self, table):
        """
        Set table for insert.
        """
        self._tables.set(table)
        return self
    
    def values(self, *args, **kwds):
        """
        Set columns and values.
        """
        if len(args) == 1 and isinstance(args[0], dict):
            self._columns = args[0].keys()
            self._values = args[0].values()
        elif kwds is not None:
            self._columns = kwds.keys()
            self._values = kwds.values()
        else:
            raise 'Values can be dictionary or keyworded variable arguments.'
        return self

