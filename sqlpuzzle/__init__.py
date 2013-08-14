# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

version = '0.20.4'
"""
Library for ease of writing SQL queries. For now only for database MySQL.
Version: %s
""" % version

import sqlpuzzle._libs.doc
import sqlpuzzle._features.functions
import sqlpuzzle._queries.delete
import sqlpuzzle._queries.insert
import sqlpuzzle._queries.select
import sqlpuzzle._queries.update


# Proxy queries.
def select(*args, **kwds):
    """Select. Set column(s) by parameter(s)."""
    return sqlpuzzle._queries.select.Select(*args, **kwds)


def selectFrom(*tables):
    """Select. Columns is set to *. Set table(s) by parameter(s)."""
    return sqlpuzzle._queries.select.Select().from_(*tables)


def insert():
    """Insert."""
    return sqlpuzzle._queries.insert.Insert()


def insertInto(table):
    """Insert. Set table by parameter."""
    return sqlpuzzle._queries.insert.Insert().into(table)


def update(table):
    """Update. Set table by parameter."""
    return sqlpuzzle._queries.update.Update(table)


def delete(*tables):
    """Delete."""
    return sqlpuzzle._queries.delete.Delete(*tables)


def deleteFrom(*args, **kwds):
    """Delete. Set table by parameter."""
    return sqlpuzzle._queries.delete.Delete().from_(*args, **kwds)


def customSql(sql):
    """Custom SQL."""
    return sqlpuzzle._libs.customSql.CustomSql(sql)


def custom(sql):
    """Alias for customSql."""
    return customSql(sql)


# Broaden doc strings of functions by useful help.
sqlpuzzle._libs.doc.doc(select, 'columns')
sqlpuzzle._libs.doc.doc(selectFrom, 'tables')


# Proxy functions.
def avg(expr):
    """Function AVG(expr)"""
    return sqlpuzzle._features.functions.Avg(expr)


def avgDistinct(expr):
    """Function AVG(DICTINCT expr)"""
    return avg(expr).distinct()


def count(expr=None):
    """Function COUNT(expr)"""
    return sqlpuzzle._features.functions.Count(expr)


def countDistinct(expr=None):
    """Function COUNT(DISTINCT expr)"""
    return count(expr).distinct()


def max(expr):
    """Function MAX(expr)"""
    return sqlpuzzle._features.functions.Max(expr)


def maxDistinct(expr):
    """Function MAX(DISTINCT expr)"""
    return max(expr).distinct()


def min(expr):
    """Function MIN(expr)"""
    return sqlpuzzle._features.functions.Min(expr)


def minDistinct(expr):
    """Function MIN(DISTINCT expr)"""
    return min(expr).distinct()


def sum(expr):
    """Function SUM(expr)"""
    return sqlpuzzle._features.functions.Sum(expr)


def sumDistinct(expr):
    """Function SUM(DISTINCT expr)"""
    return sum(expr).distinct()


def concat(*expr):
    """Function CONCAT(expr)"""
    return sqlpuzzle._features.functions.Concat(*expr)


def groupConcat(*expr):
    """Function GROUP_CONCAT(expr [ORDER BY [SEPARATOR]])"""
    return sqlpuzzle._features.functions.GroupConcat(*expr)


def convert(expr, type_=None):
    """Function CONVERT(expr, type)"""
    return sqlpuzzle._features.functions.Convert(expr, type_)
