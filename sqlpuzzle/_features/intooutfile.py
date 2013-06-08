# -*- coding: utf-8 -*-

import sqlpuzzle._libs.sqlvalue
import sqlpuzzle.exceptions


class IntoOutfile(sqlpuzzle._features.Feature):
    def __init__(self, into_outfile=None, fields_terminated_by=None, lines_terminated_by=None, optionally_enclosed_by=None):
        """Initialization of IntoOutfile."""
        self._into_outfile = into_outfile
        self._fields_terminated_by = fields_terminated_by
        self._lines_terminated_by = lines_terminated_by
        self._optionally_enclosed_by = optionally_enclosed_by

    def __str__(self):
        """Print limit (part of query)."""
        into_outfile = 'INTO OUTFILE "%s"' % self._into_outfile
        if self._fields_terminated_by is not None:
            into_outfile = '%s FIELDS TERMINATED BY %s' % (into_outfile, sqlpuzzle._libs.sqlvalue.SqlValue(self._fields_terminated_by))
        if self._lines_terminated_by is not None:
            into_outfile = '%s LINES TERMINATED BY %s' % (into_outfile, sqlpuzzle._libs.sqlvalue.SqlValue(self._lines_terminated_by))
        if self._optionally_enclosed_by is not None:
            into_outfile = '%s OPTIONALLY ENCLOSED BY %s' % (into_outfile, sqlpuzzle._libs.sqlvalue.SqlValue(self._optionally_enclosed_by))
        return into_outfile

    def __eq__(self, other):
        """Are INTO OUTFILE equivalent?"""
        return (
            self._into_outfile == other._into_outfile and
            self._fields_terminated_by == other._fields_terminated_by and
            self._lines_terminated_by == other._lines_terminated_by and
            self._optionally_enclosed_by == other._optionally_enclosed_by
        )

    def is_set(self):
        """Is intoOutfile set?"""
        return self._into_outfile is not None

    def into_outfile(self, into_outfile):
        """Set INTO OUTFILE."""
        return self._setter('into_outfile', into_outfile)

    def fields_terminated_by(self, fields_terminated_by):
        """Set FIELDS TERMINATED BY."""
        return self._setter('fields_terminated_by', fields_terminated_by)

    def lines_terminated_by(self, lines_terminated_by):
        """Set LINES TERMINATED BY."""
        return self._setter('lines_terminated_by', lines_terminated_by)

    def optionally_enclosed_by(self, optionally_enclosed_by):
        """Set OPTIONALLY ENCLOSED BY."""
        return self._setter('optionally_enclosed_by', optionally_enclosed_by)

    def _setter(self, key, value):
        """Helper for seting options."""
        if not isinstance(value, (str, unicode)):
            raise sqlpuzzle.exceptions.InvalidArgumentException()
        setattr(self, '_%s' % key, value)
        return self
