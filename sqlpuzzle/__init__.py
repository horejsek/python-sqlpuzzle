# -*- coding: utf-8 -*-

version = '0.19.1'
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


def select_from(*tables):
    """Select. Columns is set to *. Set table(s) by parameter(s)."""
    return sqlpuzzle._queries.select.Select().from_(*tables)


def insert():
    """Insert."""
    return sqlpuzzle._queries.insert.Insert()


def insert_into(table):
    """Insert. Set table by parameter."""
    return sqlpuzzle._queries.insert.Insert().into(table)


def update(table):
    """Update. Set table by parameter."""
    return sqlpuzzle._queries.update.Update(table)


def delete(*tables):
    """Delete."""
    return sqlpuzzle._queries.delete.Delete(*tables)


def delete_from(*args, **kwds):
    """Delete. Set table by parameter."""
    return sqlpuzzle._queries.delete.Delete().from_(*args, **kwds)


def customsql(sql):
    """Custom SQL."""
    return sqlpuzzle._libs.customsql.CustomSql(sql)


# Broaden doc strings of functions by useful help.
sqlpuzzle._libs.doc.doc(select, 'columns')
sqlpuzzle._libs.doc.doc(select_from, 'tables')


# Proxy functions.
def avg(expr):
    """Function AVG(expr)"""
    return sqlpuzzle._features.functions.Avg(expr)


def avg_distinct(expr):
    """Function AVG(DICTINCT expr)"""
    return avg(expr).distinct()


def count(expr=None):
    """Function COUNT(expr)"""
    return sqlpuzzle._features.functions.Count(expr)


def count_distinct(expr=None):
    """Function COUNT(DISTINCT expr)"""
    return count(expr).distinct()


def max(expr):
    """Function MAX(expr)"""
    return sqlpuzzle._features.functions.Max(expr)


def max_distinct(expr):
    """Function MAX(DISTINCT expr)"""
    return max(expr).distinct()


def min(expr):
    """Function MIN(expr)"""
    return sqlpuzzle._features.functions.Min(expr)


def min_distinct(expr):
    """Function MIN(DISTINCT expr)"""
    return min(expr).distinct()


def sum(expr):
    """Function SUM(expr)"""
    return sqlpuzzle._features.functions.Sum(expr)


def sum_distinct(expr):
    """Function SUM(DISTINCT expr)"""
    return sum(expr).distinct()


def concat(*expr):
    """Function CONCAT(expr)"""
    return sqlpuzzle._features.functions.Concat(*expr)


def group_concat(*expr):
    """Function GROUP_CONCAT(expr [ORDER BY [SEPARATOR]])"""
    return sqlpuzzle._features.functions.GroupConcat(*expr)


def convert(expr, type_=None):
    """Function CONVERT(expr, type)"""
    return sqlpuzzle._features.functions.Convert(expr, type_)
