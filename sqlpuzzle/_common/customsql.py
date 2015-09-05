# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .object import Object
from .utils import force_text

__all__ = ('CustomSql',)


class CustomSql(Object):
    """
    Or ``sqlpuzzle.customsql``.

    Force custom SQL if it's not supported by ``sqlpuzzle``.

    .. code-block:: python

        >>> sqlpuzzle.select(sqlpuzzle.C('IFNULL(col, 42) AS col'))
        <Select: SELECT IFNULL(col, 42) AS col>
        >>> sqlpuzzle.update('t').set(sqlpuzzle.C('`age` = `age` + 1')).where(id=42)
        <Update: UPDATE "t" SET `age` = `age` + 1 WHERE "id" = 42>
    """

    def __init__(self, string=''):
        super(CustomSql, self).__init__()
        self._custom_sql_string = force_text(string)

    def __unicode__(self):
        return self._custom_sql_string
