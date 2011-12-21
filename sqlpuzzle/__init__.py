# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle._libs.doc
import sqlpuzzle._features.functions
import sqlpuzzle._queries.delete
import sqlpuzzle._queries.insert
import sqlpuzzle._queries.select
import sqlpuzzle._queries.update


# Proxy queries.
def select(*columns):
    """Select. Set column(s) by parameter(s)."""
    return sqlpuzzle._queries.select.Select(*columns)


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


def delete():
    """Delete."""
    return sqlpuzzle._queries.delete.Delete()


def deleteFrom(table):
    """Delete. Set table by parameter."""
    return sqlpuzzle._queries.delete.Delete().from_(table)


def customSql(text):
    """Custom SQL."""
    return sqlpuzzle._libs.customSql.CustomSql(text)


# Broaden doc strings of functions by useful help.
sqlpuzzle._libs.doc.doc(select, 'columns')
sqlpuzzle._libs.doc.doc(selectFrom, 'tables')


# Proxy functions.
def avg(expr):
    """Function AVG"""
    return sqlpuzzle._features.functions.Avg(expr)


def count(expr=None):
    """Function COUNT"""
    return sqlpuzzle._features.functions.Count(expr)


def max(expr):
    """Function MAX"""
    return sqlpuzzle._features.functions.Max(expr)


def min(expr):
    """Function MIN"""
    return sqlpuzzle._features.functions.Min(expr)


def sum(expr):
    """Function SUM"""
    return sqlpuzzle._features.functions.Sum(expr)

