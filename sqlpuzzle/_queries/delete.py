# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

import sqlpuzzle.exceptions

import sqlpuzzle._libs.doc
import sqlpuzzle._features.tables
import sqlpuzzle._features.where


class Delete(sqlpuzzle._queries.Query):
    def __init__(self):
        """Initialization of Delete."""
        super(Delete, self).__init__()

        self._setFeatures(
            tables = sqlpuzzle._features.tables.Tables(),
            where = sqlpuzzle._features.where.Where(),
        )
        self._setKeysOfFeaturesForAutoPrinting('where')

        self.__allowDeleteAll = False

    def copy(self):
        """Create copy."""
        newQuery = super(Delete, self).copy()
        if self.__allowDeleteAll:
            newQuery.allowDeleteAll()
        else:
            newQuery.forbidDeleteAll()
        return newQuery

    def __str__(self):
        """Print query."""
        if not self._where.isSet() and not self.__allowDeleteAll:
            raise sqlpuzzle.exceptions.ConfirmDeleteAllException()

        delete = "DELETE FROM %s" % (
            str(self._tables),
        )
        return super(Delete, self)._printFeatures(delete)

    def allowDeleteAll(self):
        """Allow delete all records."""
        self.__allowDeleteAll = True
        return self

    def forbidDeleteAll(self):
        """Forbid delete all records."""
        self.__allowDeleteAll = False
        return self

    def from_(self, *tables):
        """Set table(s) to query."""
        self._tables.set(tables)
        return self

    def where(self, *args, **kwds):
        """Set condition(s) to query."""
        self._where.where(*args, **kwds)
        return self

    # Broaden doc strings of functions by useful help.
    sqlpuzzle._libs.doc.doc(from_, 'tables')
    sqlpuzzle._libs.doc.doc(where, 'where')
