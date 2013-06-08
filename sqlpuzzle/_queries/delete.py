# -*- coding: utf-8 -*-

import sqlpuzzle.exceptions

import sqlpuzzle._libs.doc
import sqlpuzzle._features.tables
import sqlpuzzle._features.where


class Delete(sqlpuzzle._queries.Query):
    def __init__(self, *tables):
        """Initialization of Delete."""
        super(Delete, self).__init__()

        self._set_features(
            tables=sqlpuzzle._features.tables.Tables(),
            references=sqlpuzzle._features.tables.Tables(),
            where=sqlpuzzle._features.where.Where(),
        )
        self._set_keys_of_features_for_auto_printing('where')

        self.__allow_delete_all = False

        self._tables.set(*tables)

    def copy(self):
        """Create copy."""
        new_query = super(Delete, self).copy()
        if self.__allow_delete_all:
            new_query.allow_delete_all()
        else:
            new_query.forbid_delete_all()
        return new_query

    def __str__(self):
        """Print query."""
        if not self._where.is_set() and not self.__allow_delete_all:
            raise sqlpuzzle.exceptions.ConfirmDeleteAllException()

        delete = "DELETE %sFROM %s" % (
            '%s ' % self._tables if self._tables.is_set() else '',
            str(self._references),
        )
        return super(Delete, self)._print_features(delete)

    def allow_delete_all(self):
        """Allow delete all records."""
        self.__allow_delete_all = True
        return self

    def forbid_delete_all(self):
        """Forbid delete all records."""
        self.__allow_delete_all = False
        return self

    def delete(self, *tables):
        """Set table(s) name to delete."""
        self._tables.set(*tables)
        return self

    def from_(self, *args, **kwds):
        """Set reference table(s) to query."""
        self._references.set(*args, **kwds)
        return self

    def from_table(self, table, alias=None):
        """Set reference table to query."""
        self._references.set((table, alias))
        return self

    def from_tables(self, *args, **kwds):
        """Alias for method `from_`."""
        self.from_(*args, **kwds)
        return self

    def join(self, table):
        """Join reference table."""
        self._references.join(table)
        return self

    def inner_join(self, table):
        """Inner join reference table."""
        self._references.inner_join(table)
        return self

    def left_join(self, table):
        """Left join reference table."""
        self._references.left_join(table)
        return self

    def right_join(self, table):
        """Right join reference table."""
        self._references.right_join(table)
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
