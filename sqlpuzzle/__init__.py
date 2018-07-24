"""
Library for ease of writing SQL queries. For now only for database MySQL & PostgreSQL.
"""

# pylint: disable=redefined-builtin

from .version import VERSION
from ._backends import set_backend
from ._common import CustomSql as customsql, SqlValue as sqlvalue, SqlReference as sqlreference
from ._queryparts import Not
from ._queryparts.functions import Avg, Concat, Convert, Count, GroupConcat, Max, Min, Sum
from ._queryparts.conditions import Conditions
from ._queries import Delete, Insert, Select, Update

__all__ = (
    'configure',

    'select',
    'select_from',
    'insert',
    'insert_into',
    'update',
    'delete',
    'delete_from',
    'customsql',

    'Q',
    'customsql',
    'C',
    'sqlvalue',
    'V',
    'sqlreference',
    'R',

    'Not',

    'avg',
    'avg_distinct',
    'count',
    'count_distinct',
    'max',
    'max_distinct',
    'min',
    'min_distinct',
    'sum',
    'sum_distinct',
    'concat',
    'group_concat',
    'convert',
)


def configure(database):
    """
    By default sqlpuzzle generates syntax in plain SQL. If you want to change it,
    you should call this method somewhere on start of your app. For now there is
    only support of SQLite, MySQL and PostgreSQL.

    .. code-block:: python

        configure('sqlite')
        # or
        configure('mysql')
        # or
        configure('postgresql')
    """
    set_backend(database)


def select(*args, **kwds):
    """
    Returns :py:class:`~.Select` instance and passed arguments are used for list
    of columns.
    """
    return Select(*args, **kwds)


def select_from(*args, **kwds):
    """
    Returns :py:class:`~.Select` instance and passed arguments are used for list
    of tables. Columns are set to `*`.
    """
    return Select().from_(*args, **kwds)


def insert():
    """
    Returns :py:class:`~.Insert` instance. But probably you want to use
    :py:func:`~.insert_into` instead.
    """
    return Insert()


def insert_into(table):
    """
    Returns :py:class:`~.Insert` instance and passed argument is used for table.
    """
    return Insert().into(table)


def update(table):
    """
    Returns :py:class:`~.Update` instance and passed argument is used for table.
    """
    return Update(table)


def delete(*tables):
    """
    Returns :py:class:`~.Delete` instance and passed arguments are used for list
    of tables from which really data should be deleted. But probably you want
    to use :py:func:`~.delete_from` instead.
    """
    return Delete(*tables)


def delete_from(*args, **kwds):
    """
    Returns :py:class:`~.Delete` instance and passed arguments are used for list
    of tables.
    """
    return Delete().from_(*args, **kwds)


def Q(*args, **kwds):
    """
    Use as condition (where, having, ...) and pass it to condition. Works like
    Q object in Django, so you can use it with logical operands (& and |).

    .. code-block:: python

        sqlpuzzle.where(Q(name='Michael', country=None) | Q(name='Alan'))
    """
    return Conditions(*args, **kwds)


def avg(expr):
    """
    Function ``AVG(expr)``
    """
    return Avg(expr)


def avg_distinct(expr):
    """
    Function ``AVG(DICTINCT expr)``
    """
    return avg(expr).distinct()


def count(expr=None):
    """
    Function ``COUNT(expr)``
    """
    return Count(expr)


def count_distinct(expr=None):
    """
    Function ``COUNT(DISTINCT expr)``
    """
    return count(expr).distinct()


def max(expr):
    """
    Function ``MAX(expr)``
    """
    return Max(expr)


def max_distinct(expr):
    """
    Function ``MAX(DISTINCT expr)``
    """
    return max(expr).distinct()


def min(expr):
    """
    Function ``MIN(expr)``
    """
    return Min(expr)


def min_distinct(expr):
    """
    Function ``MIN(DISTINCT expr)``
    """
    return min(expr).distinct()


def sum(expr):
    """
    Function ``SUM(expr)``
    """
    return Sum(expr)


def sum_distinct(expr):
    """
    Function ``SUM(DISTINCT expr)``
    """
    return sum(expr).distinct()


def concat(*expr):
    """
    Function ``CONCAT(expr)``
    """
    return Concat(*expr)


def group_concat(*expr):
    """
    Function ``GROUP_CONCAT(expr [ORDER BY [SEPARATOR]])``

    :return: :py:class:`~.GroupConcat`
    """
    return GroupConcat(*expr)


def convert(expr, type_=None):
    """
    Function ``CONVERT(expr, type)``

    :return: :py:class:`~.Convert`
    """
    return Convert(expr, type_)


# Shortcuts.


C = customsql
V = sqlvalue
R = sqlreference
