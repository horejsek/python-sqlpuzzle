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
    def __init__(self, *tables):
        """Initialization of Delete."""
        super(Delete, self).__init__()

        self._setFeatures(
            tables = sqlpuzzle._features.tables.Tables(),
            references = sqlpuzzle._features.tables.Tables(),
            where = sqlpuzzle._features.where.Where(),
        )
        self._setKeysOfFeaturesForAutoPrinting('where')

        self.__allowDeleteAll = False

        self._tables.set(*tables)

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

        delete = "DELETE %sFROM %s" % (
            '%s ' % self._tables if self._tables.isSet() else '',
            str(self._references),
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

    def delete(self, *tables):
        """Set table(s) name to delete."""
        self._tables.set(*tables)
        return self

    def from_(self, *args, **kwds):
        """Set reference table(s) to query."""
        self._references.set(*args, **kwds)
        return self

    def fromTable(self, table, alias=None):
        """Set reference table to query."""
        self._references.set((table, alias))
        return self

    def fromTables(self, *args, **kwds):
        """Alias for method `from_`."""
        self.from_(*args, **kwds)
        return self

    def join(self, table):
        """Join reference table."""
        self._references.join(table)
        return self

    def innerJoin(self, table):
        """Inner join reference table."""
        self._references.innerJoin(table)
        return self

    def leftJoin(self, table):
        """Left join reference table."""
        self._references.leftJoin(table)
        return self

    def rightJoin(self, table):
        """Right join reference table."""
        self._references.rightJoin(table)
        return self

    def on(self, *args, **kwds):
        """Join on."""
        self._references.on(*args, **kwds)
        return self

    def where(self, *args, **kwds):
        """Set condition(s) to query."""
        self._where.where(*args, **kwds)
        return self

    # Broaden doc strings of functions by useful help.
    sqlpuzzle._libs.doc.doc(from_, 'tables')
    sqlpuzzle._libs.doc.doc(where, 'where')
