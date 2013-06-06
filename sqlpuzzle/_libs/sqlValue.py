# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

import types
import datetime
import re

import sqlpuzzle._features
import sqlpuzzle._queries
import sqlpuzzle.exceptions


class SqlValue(object):
    """Object used for SQL values (e.g. value of column, for condition, ...)."""

    def __init__(self, value):
        """Initialization of SqlValue."""
        self._map = {
            str: self._string,
            unicode: self._string,
            int: self._integer,
            long: self._integer,
            float: self._float,
            bool: self._boolean,
            datetime.date: self._date,
            datetime.datetime: self._datetime,
            list: self._list,
            tuple: self._list,
            set: self._list,
            frozenset: self._list,
            types.NoneType: self._null,
            xrange: self._list,
            types.GeneratorType: self._list,
            sqlpuzzle._queries.select.Select: self._subselect,
            sqlpuzzle._queries.union.Union: self._subselect,
            sqlpuzzle._libs.customSql.CustomSql: self._raw,
        }

        self.value = value

    def __repr__(self):
        return "<SqlValue: %s>" % self.__str__()

    def __str__(self):
        """Convert and print value."""
        return self._getConvertMethod()()

    def _getConvertMethod(self):
        """Get right method to convert of the value."""
        for type_, method in self._map.iteritems():
            if isinstance(self.value, type_):
                return method
        return self._undefined

    def _raw(self):
        """No convert."""
        return str(self.value)

    def _string(self):
        """Convert as string."""
        # sometime, e.g. in subselect, is needed reference to column instead of self.value
        if self.value.strip() and self.value.strip()[0] == '`':
            return self._backQuotes()
        return '"%s"' % self._escapeValue(self.value)

    def _integer(self):
        """Convert as integer."""
        return '%d' % self.value

    def _float(self):
        """Convert as float."""
        return '%.5f' % self.value

    def _boolean(self):
        """Convert as boolean."""
        return '%d' % self.value

    def _date(self):
        """Convert as date."""
        return self._datetime()

    def _datetime(self):
        """Convert as datetime."""
        return '"%s"' % self.value.isoformat()

    def _list(self):
        """Convert as list of values."""
        if self.value:
            return "(%s)" % ", ".join(str(SqlValue(item)) for item in self.value)
        raise sqlpuzzle.exceptions.InvalidArgumentException('Empty list is not allowed.')

    def _subselect(self):
        """Convert as subselect."""
        return "(%s)" % self.value

    def _null(self):
        """NULL"""
        return 'NULL'

    def _undefined(self):
        """undefined"""
        return '<undefined value>'

    def _escapeValue(self, value):
        replaceTable = (
            ("\\", "\\\\"),
            ('"', '\\"'),
            ("'", "\\'"),
            ("\n", "\\n"),
        )
        for old, new in replaceTable:
            value = value.replace(old, new)
        return value

    def _backQuotes(self):
        """
        Convert as reference on column.
        "table" => "`table`"
        "table.column" => "`table`.`column`"
        "db.table.column" => "`db`.`table`.`column`"
        "table.`col.umn`" => "`table`.`col.umn`"
        "`table`.`col.umn`" => "`table`.`col.umn`"
        """
        return '.'.join('`%s`' % i if i != '*' else i for i in re.split('`([^`]+)`|\.', self.value) if i)



class SqlReference(SqlValue):
    """Object used for string for SQL reference (e.g. name of tables, columns, ...)."""

    def __init__(self, value):
        """Initialization of SqlReference."""
        self._map = {
            str: self._backQuotes,
            unicode: self._backQuotes,
            int: self._integer,
            sqlpuzzle._queries.select.Select: self._subselect,
            sqlpuzzle._queries.union.Union: self._subselect,
            sqlpuzzle._features.functions.Function: self._raw,
            sqlpuzzle._libs.customSql.CustomSql: self._raw,
        }

        self.value = value
