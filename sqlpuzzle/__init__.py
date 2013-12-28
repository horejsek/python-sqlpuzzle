# -*- coding: utf-8 -*-

from __future__ import absolute_import

VERSION = '1.1.0'
"""
Library for ease of writing SQL queries. For now only for database MySQL.
Version: %s
""" % VERSION

from ._backends import set_backend
from ._common import CustomSql as customsql, SqlValue as sqlvalue, SqlReference as sqlreference
from ._queryparts.functions import Avg, Concat, Convert, Count, GroupConcat, Max, Min, Sum
from ._queryparts.conditions import Conditions
from ._queries import Delete, Insert, Select, Update

__all__ = (
    'configure',

    'select'
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
    Configure used database, so sqlpuzzle can generate queries which are needed.
    For now there is only support of MySQL and PostgreSQL.
    configure('mysql')
    configure('postgresql')
    """
    set_backend(database)


def select(*args, **kwds):
    """Select. Set column(s) by parameter(s).
    select('id', 'name', ...)
    select(('id', 'asId'), ('name', 'asName'))
    select({'id': 'asId', 'name': 'asName'})
    """
    return Select(*args, **kwds)


def select_from(*args, **kwds):
    """Select. Columns is set to *. Set table(s) by parameter(s).
    select_from('user', 'country', ...)
    select_from(('user', 'asUser'), ('user', 'asParent'))
    select_from({'user': 'asUser', 'user', 'asParent'})
    """
    return Select().from_(*args, **kwds)


def insert():
    """Insert."""
    return Insert()


def insert_into(table):
    """Insert. Set table by parameter."""
    return Insert().into(table)


def update(table):
    """Update. Set table by parameter."""
    return Update(table)


def delete(*tables):
    """Delete."""
    return Delete(*tables)


def delete_from(*args, **kwds):
    """Delete. Set table by parameter.
    delete_from('user', 'country', ...)
    delete_from(('user', 'asUser'), ('user', 'asParent'))
    delete_from({'user': 'asUser', 'user', 'asParent'})
    """
    return Delete().from_(*args, **kwds)


def Q(**kwds):
    """
    Use as condition (where, having, ...) and pass it to condition. Works like
    Q object in Django, so you can use it with logical operands (& and |).

    Fro example:
    sqlpuzzle.where(Q(name='Michael', country=None) | Q(name='Alan'))
    """
    return Conditions(**kwds)


def avg(expr):
    """Function AVG(expr)"""
    return Avg(expr)


def avg_distinct(expr):
    """Function AVG(DICTINCT expr)"""
    return avg(expr).distinct()


def count(expr=None):
    """Function COUNT(expr)"""
    return Count(expr)


def count_distinct(expr=None):
    """Function COUNT(DISTINCT expr)"""
    return count(expr).distinct()


def max(expr):
    """Function MAX(expr)"""
    return Max(expr)


def max_distinct(expr):
    """Function MAX(DISTINCT expr)"""
    return max(expr).distinct()


def min(expr):
    """Function MIN(expr)"""
    return Min(expr)


def min_distinct(expr):
    """Function MIN(DISTINCT expr)"""
    return min(expr).distinct()


def sum(expr):
    """Function SUM(expr)"""
    return Sum(expr)


def sum_distinct(expr):
    """Function SUM(DISTINCT expr)"""
    return sum(expr).distinct()


def concat(*expr):
    """Function CONCAT(expr)"""
    return Concat(*expr)


def group_concat(*expr):
    """Function GROUP_CONCAT(expr [ORDER BY [SEPARATOR]])"""
    return GroupConcat(*expr)


def convert(expr, type_=None):
    """Function CONVERT(expr, type)"""
    return Convert(expr, type_)


# Shortcuts.


C = customsql
V = sqlvalue
R = sqlreference


# Backward compatibility.

selectFrom = select_from
insertInto = insert_into
deleteFrom = delete_from
custom = customSql = customsql
avgDistinct = avg_distinct
countDistinct = count_distinct
minDistinct = min_distinct
sumDistinct = sum_distinct
groupConcat = group_concat
