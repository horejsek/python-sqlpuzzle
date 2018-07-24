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
        ("'", "''"),
        ("\n", "\\n"),
    )
    for old, new in replace_table:
        value = value.replace(old, new)
    return value


class SqlValue(Object):
    """
    Or ``sqlpuzzle.sqlvalue``.

    SQL values which are escaped. Like values in conditions. SqlPuzzle by default
    behave to some arguments automatically as SQL value and to some as SQL reference.
    Use this when SqlPuzzle uses SQL reference instead of value.

    .. code-block:: python

        >>> sqlpuzzle.select('a')
        <Select: SELECT `a`>
        >>> sqlpuzzle.select(sqlpuzzle.V('a'))
        <Select: SELECT 'a'>
    """

    def __init__(self, value):
        from sqlpuzzle._queries import Select, Union
        self._map = {
            str: self._string,
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
            range: self._list,
            types.GeneratorType: self._list,
            Select: self._subselect,
            Union: self._subselect,
        }

        self.value = value

    def __str__(self):
        convert_method = self._get_convert_method()
        return convert_method()

    def _get_convert_method(self):
        """
        Get right method to convert of the value.
        """
        for type_, method in self._map.items():
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
        return "'{}'".format(_escape_value(force_text(self.value)))

    def _integer(self):
        return '{:d}'.format(self.value)

    def _float(self):
        return '{:.5f}'.format(self.value)

    def _boolean(self):
        return get_backend().boolean(self.value)

    def _date(self):
        return self._datetime()

    def _datetime(self):
        return "'{}'".format(self.value.isoformat())

    def _list(self):
        if self.value:
            return '({})'.format(', '.join(force_text(SqlValue(item)) for item in self.value))
        raise InvalidArgumentException('Empty list is not allowed.')

    def _subselect(self):
        return '({})'.format(self.value)

    def _null(self):
        return 'NULL'

    def _undefined(self):
        try:
            return '<undefined value {}>'.format(self.value)
        except Exception:
            return '<undefined value>'

    def _reference(self):
        return get_backend().reference(self.value)


class SqlReference(SqlValue):
    """
    Or ``sqlpuzzle.sqlreference``.

    SQL reference is some column. SqlPuzzle by default behave to some arguments
    automatically as SQL value and to some as SQL reference. Use this when SqlPuzzle
    uses SQL value instead of reference.

    .. code-block:: python

        >>> sqlpuzzle.select_from('t').where(name='surname')
        <Select: SELECT * FROM `t` WHERE `name` = 'surname'>
        >>> sqlpuzzle.select_from('t').where(name=sqlpuzzle.R('surname'))
        <Select: SELECT * FROM `t` WHERE `name` = `surname`>
    """

    def __init__(self, value):
        from sqlpuzzle._queries import Select, Union
        self._map = {
            str: self._reference,
            int: self._integer,
            Select: self._subselect,
            Union: self._subselect,
        }

        self.value = value
