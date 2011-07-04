# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle.queries.delete
import sqlpuzzle.queries.insert
import sqlpuzzle.queries.select
import sqlpuzzle.queries.update


def select(*columns):
    """
    Select.
    Params are strings or list of columns to select.
    """
    return sqlpuzzle.queries.select.Select(*columns)


def selectFrom(table):
    """
    Select.
    Param is table, column is set to *.
    """
    return sqlpuzzle.queries.select.Select().from_(table)


def insert():
    """
    Insert.
    """
    return sqlpuzzle.queries.insert.Insert()


def insertInto(table):
    """
    Insert.
    Param is table.
    """
    return sqlpuzzle.queries.insert.Insert().into(table)


def update(table):
    """
    Update.
    Param is table.
    """
    return sqlpuzzle.queries.update.Update(table)


def delete():
    """
    Delete.
    """
    return sqlpuzzle.queries.delete.Delete()


def deleteFrom(table):
    """
    Delete.
    Param is table.
    """
    return sqlpuzzle.queries.delete.Delete().from_(table)


