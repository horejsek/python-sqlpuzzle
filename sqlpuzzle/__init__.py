# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle._queries.delete
import sqlpuzzle._queries.insert
import sqlpuzzle._queries.select
import sqlpuzzle._queries.update


def select(*columns):
    """Select.
    Params are strings or list of columns to select.
    """
    return sqlpuzzle._queries.select.Select(*columns)


def selectFrom(*tables):
    """Select.
    Param is table, column is set to *.
    """
    return sqlpuzzle._queries.select.Select().from_(*tables)


def insert():
    """Insert."""
    return sqlpuzzle._queries.insert.Insert()


def insertInto(table):
    """Insert.
    Param is table.
    """
    return sqlpuzzle._queries.insert.Insert().into(table)


def update(table):
    """Update.
    Param is table.
    """
    return sqlpuzzle._queries.update.Update(table)


def delete():
    """Delete."""
    return sqlpuzzle._queries.delete.Delete()


def deleteFrom(table):
    """Delete.
    Param is table.
    """
    return sqlpuzzle._queries.delete.Delete().from_(table)


def customSql(text):
    """Custom SQL."""
    return sqlpuzzle._libs.customSql.CustomSql(text)

