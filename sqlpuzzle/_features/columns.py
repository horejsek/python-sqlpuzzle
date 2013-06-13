# -*- coding: utf-8 -*-

import sqlpuzzle._libs.argsparser
import sqlpuzzle._libs.sqlvalue
import sqlpuzzle._libs.customsql

import sqlpuzzle._features.functions


class Column(sqlpuzzle._features.Feature):
    def __init__(self, column=None, as_=None):
        """Initialization of Column."""
        super(Column, self).__init__()
        self._column = column
        self._as = as_

    def __str__(self):
        """Print part of query."""
        if self._as:
            return '%s AS %s' % (
                sqlpuzzle._libs.sqlvalue.SqlReference(self._column),
                sqlpuzzle._libs.sqlvalue.SqlReference(self._as),
            )
        else:
            return str(sqlpuzzle._libs.sqlvalue.SqlReference(self._column))

    def __eq__(self, other):
        """Are columns equivalent?"""
        return (
            self._column == other._column and
            self._as == other._as
        )


class Columns(sqlpuzzle._features.Features):
    def __init__(self):
        """Initialization of Columns."""
        super(Columns, self).__init__()
        self._default_query_string = '*'

    def columns(self, *args, **kwds):
        """Set columns."""
        allowed_data_types = sqlpuzzle._libs.argsparser.AllowedDataTypes().add(
            (int, str, unicode, sqlpuzzle._queries.select.Select, sqlpuzzle._queries.union.Union,
             sqlpuzzle._libs.customsql.CustomSql, sqlpuzzle._features.functions.Function),
            (str, unicode)
        ).add(
            sqlpuzzle._libs.customsql.CustomSql
        )

        for column_name, as_ in sqlpuzzle._libs.argsparser.parse_args_to_list_of_tuples(
            {
                'max_items': 2,
                'allow_dict': True,
                'allowed_data_types': allowed_data_types,
            },
            *args,
            **kwds
        ):
            column = Column(column_name, as_)
            if column not in self:
                self.append_feature(column)

        return self
