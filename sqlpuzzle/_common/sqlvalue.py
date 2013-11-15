# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six
from six.moves import xrange
try:
    long
except NameError:
    long = int

import datetime
import decimal
import types

from sqlpuzzle.exceptions import InvalidArgumentException
from sqlpuzzle._backends import get_backend
from .object import Object
from .utils import force_text, is_sql_instance

__all__ = ('SqlValue', 'SqlReference')


def _escape_value(value):
    replace_table = (
        ("\\", "\\\\"),
        ("'", "\\'"),
        ("\n", "\\n"),
    )
    for old, new in replace_table:
        value = value.replace(old, new)
    return value


class SqlValue(Object):
    """Object used for SQL values (e.g. value of column, for condition, ...)."""

    def __init__(self, value):
        from sqlpuzzle._queries import Select, Union
        self._map = {
            str: self._string,
            six.text_type: self._string,
            int: self._integer,
            long: self._integer,
            float: self._float,
            decimal.Decimal: self._float,
            bool: self._boolean,
            datetime.date: self._date,
            datetime.datetime: self._datetime,
            list: self._list,
            tuple: self._list,
            set: self._list,
            frozenset: self._list,
            type(None): self._null,
            xrange: self._list,
            types.GeneratorType: self._list,
            Select: self._subselect,
            Union: self._subselect,
        }

        self.value = value

    def __unicode__(self):
        convert_method = self._get_convert_method()
        return convert_method()

    def _get_convert_method(self):
        """Get right method to convert of the value."""
        for type_, method in six.iteritems(self._map):
            if type(self.value) is bool and type_ is not bool:
                continue
            if isinstance(self.value, type_):
                return method
        if is_sql_instance(self.value):
            return self._raw
        return self._undefined

    def _raw(self):
        return force_text(self.value)

    def _string(self):
        # Sometimes, e.g. in subselect, is needed reference to column instead of self.value.
        if get_backend().is_reference(self.value):
            return self._reference()
        return six.u("'%s'") % _escape_value(force_text(self.value))

    def _integer(self):
        return six.u('%d') % self.value

    def _float(self):
        return six.u('%.5f') % self.value

    def _boolean(self):
        return get_backend().boolean(self.value)

    def _date(self):
        return self._datetime()

    def _datetime(self):
        return six.u("'%s'") % self.value.isoformat()

    def _list(self):
        if self.value:
            return six.u('(%s)') % six.u(', ').join(force_text(SqlValue(item)) for item in self.value)
        raise InvalidArgumentException('Empty list is not allowed.')

    def _subselect(self):
        return six.u('(%s)') % self.value

    def _null(self):
        return six.u('NULL')

    def _undefined(self):
        try:
            return six.u('<undefined value %s>') % self.value
        except Exception:
            return six.u('<undefined value>')

    def _reference(self):
        return get_backend().reference(self.value)


class SqlReference(SqlValue):
    """Object used for string for SQL reference (e.g. name of tables, columns, ...)."""

    def __init__(self, value):
        from sqlpuzzle._queries import Select, Union
        self._map = {
            str: self._reference,
            six.text_type: self._reference,
            int: self._integer,
            Select: self._subselect,
            Union: self._subselect,
        }

        self.value = value
