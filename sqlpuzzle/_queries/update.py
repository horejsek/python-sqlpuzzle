# -*- coding: utf-8 -*-

import sqlpuzzle.exceptions

import sqlpuzzle._libs.doc
import sqlpuzzle._features.tables
import sqlpuzzle._features.values
import sqlpuzzle._features.where


class Update(sqlpuzzle._queries.Query):
    def __init__(self, table=None):
        """Initialization of Update."""
        super(Update, self).__init__()

        self._set_features(
            tables=sqlpuzzle._features.tables.Tables(),
            values=sqlpuzzle._features.values.Values(),
            where=sqlpuzzle._features.where.Where(),
        )
        self._set_keys_of_features_for_auto_printing('where')

        self.__allow_update_all = False
        self.table(table)

    def copy(self):
        """Create copy."""
        new_query = super(Update, self).copy()
        if self.__allow_update_all:
            new_query.allow_update_all()
        else:
            new_query.forbid_update_all()
        return new_query

    def __str__(self):
        """Print query."""
        if not self._where.is_set() and not self.__allow_update_all:
            raise sqlpuzzle.exceptions.ConfirmUpdateAllException()

        update = "UPDATE %s SET %s" % (
            str(self._tables),
            str(self._values),
        )
        return super(Update, self)._print_features(update)

    def allow_update_all(self):
        """Allow update all records."""
        self.__allow_update_all = True
        return self

    def forbid_update_all(self):
        """Forbid update all records."""
        self.__allow_update_all = False
        return self

    def table(self, table):
        """Set table."""
        self._tables.set(table)
        return self

    def set(self, *args, **kwds):
        """Set columns and values."""
        self._values.set(*args, **kwds)
        return self

    def where(self, *args, **kwds):
        """Set condition(s) to query."""
        self._where.where(*args, **kwds)
        return self

    # Broaden doc strings of functions by useful help.
    sqlpuzzle._libs.doc.doc(table, 'tables')
    sqlpuzzle._libs.doc.doc(set, 'values')
    sqlpuzzle._libs.doc.doc(where, 'where')
