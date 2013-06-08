# -*- coding: utf-8 -*-

import sqlpuzzle._libs.doc
import sqlpuzzle._features.tables
import sqlpuzzle._features.onduplicatekeyupdate
import sqlpuzzle._features.values


class Insert(sqlpuzzle._queries.Query):
    def __init__(self):
        """Initialization of Insert."""
        super(Insert, self).__init__()

        self._set_features(
            tables=sqlpuzzle._features.tables.Tables(),
            values=sqlpuzzle._features.values.MultipleValues(),
            on_duplicate_key_update=sqlpuzzle._features.onduplicatekeyupdate.OnDuplicateKeyUpdate(
            ),
        )
        self._set_keys_of_features_for_auto_printing('on_duplicate_key_update')

    def __str__(self):
        """Print query."""
        insert = "INSERT INTO %s %s" % (
            str(self._tables),
            str(self._values),
        )
        return super(Insert, self)._print_features(insert)

    def into(self, table):
        """Set table for insert."""
        self._tables.set(table)
        return self

    def values(self, *args, **kwds):
        """Set columns and values."""
        self._values.add(*args, **kwds)
        return self

    def on_duplicate_key_update(self, *args, **kwds):
        """Set on duplicate key update."""
        self._on_duplicate_key_update.set(*args, **kwds)
        return self

    # Broaden doc strings of functions by useful help.
    sqlpuzzle._libs.doc.doc(into, 'tables')
    sqlpuzzle._libs.doc.doc(values, 'values')
