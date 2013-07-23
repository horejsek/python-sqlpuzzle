# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

import sqlpuzzle._libs.argsParser
import sqlpuzzle._libs.sqlValue
import sqlpuzzle._libs.customSql

import sqlpuzzle._features.functions


class Column(sqlpuzzle._features.Feature):
    def __init__(self, column=None, as_=None):
        """Initialization of Column."""
        self._column = column
        self._as = as_

    def __str__(self):
        """Print part of query."""
        if self._as:
            return '%s AS %s' % (
                sqlpuzzle._libs.sqlValue.SqlReference(self._column),
                sqlpuzzle._libs.sqlValue.SqlReference(self._as),
            )
        else:
            return str(sqlpuzzle._libs.sqlValue.SqlReference(self._column))

    def __eq__(self, other):
        """Are columns equivalent?"""
        return (
            type(self) == type(other) and
            self._column == other._column and
            self._as == other._as
        )


class Columns(sqlpuzzle._features.Features):
    def __init__(self):
        """Initialization of Columns."""
        super(Columns, self).__init__()
        self._defaultQueryString = '*'

    def columns(self, *args, **kwds):
        """Set columns."""

        allowedDataTypes = sqlpuzzle._libs.argsParser.AllowedDataTypes().add(
            (int, str, unicode, sqlpuzzle._queries.select.Select, sqlpuzzle._queries.union.Union, sqlpuzzle._libs.customSql.CustomSql, sqlpuzzle._features.functions.Function),
            (str, unicode)
        ).add(
            sqlpuzzle._libs.customSql.CustomSql
        )

        for columnName, as_ in sqlpuzzle._libs.argsParser.parseArgsToListOfTuples(
            {
                'maxItems': 2,
                'allowDict': True,
                'allowedDataTypes': allowedDataTypes,
            },
            *args,
            **kwds
        ):
            column = Column(columnName, as_)
            if column not in self:
                self.appendFeature(column)

        return self
