# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import query


class Update(query.Query):
    def __init__(self, table=None):
        """
        Initialization of Update.
        """
        query.Query.__init__(self)
        self.table(table)
        self._columns = None
        self._values = None
    
    def __str__(self):
        """
        Print query.
        """
        update = "UPDATE %s SET %s" % (
            str(self._tables),
            ', '.join(('`%s` = "%s"' % (column, value) for column, value in zip(self._columns, self._values)))
        )
        if self._conditions.isSet(): update = "%s %s" % (update, self._conditions)
        
        return update
    
    def _typeOfQuery(self):
        return 'UPDATE'
    
    def table(self, table):
        """
        Set table.
        """
        self._tables.set(table)
        return self
    
    def set(self, *args, **kwargs):
        """
        Set columns and values.
        """
        if len(args) == 1 and isinstance(args[0], dict):
            self._columns = args[0].keys()
            self._values = args[0].values()
        elif kwargs is not None:
            self._columns = kwargs.keys()
            self._values = kwargs.values()
        else:
            raise 'Values can be dictionary or keyworded variable arguments.'
        return self
    
    def where(self, *args, **kwargs):
        """
        Set condition(s) to query.
        """
        self._conditions.where(*args, **kwargs)
        return self

