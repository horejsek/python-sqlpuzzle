# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import query


class Delete(query.Query):
    def __init__(self):
        """
        Initialization of Delete.
        """
        query.Query.__init__(self)
    
    def __str__(self):
        """
        Print query.
        """
        delete = "DELETE FROM %s" % (
            str(self._tables),
        )
        if self._conditions.isSet(): delete = "%s %s" % (delete, self._conditions)
        
        return delete
    
    def _typeOfQuery(self):
        return 'DELETE'
    
    def from_(self, *tables):
        """
        Set table(s) to query.
        """
        self._tables.set(tables)
        return self
    
    def where(self, *args, **kwds):
        """
        Set condition(s) to query.
        """
        self._conditions.where(*args, **kwds)
        return self

