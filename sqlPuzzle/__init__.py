# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.queries.delete
import sqlPuzzle.queries.insert
import sqlPuzzle.queries.select
import sqlPuzzle.queries.update


def select(*columns):
    """
    Select.
    Params are strings or list of columns to select.
    """
    return sqlPuzzle.queries.select.Select(*columns)


def selectFrom(table):
    """
    Select.
    Param is table, column is set to *.
    """
    return sqlPuzzle.queries.select.Select().from_(table)


def insert():
    """
    Insert.
    """
    return sqlPuzzle.queries.insert.Insert()


def insertInto(table):
    """
    Insert.
    Param is table.
    """
    return sqlPuzzle.queries.insert.Insert().into(table)


def update(table):
    """
    Update.
    Param is table.
    """
    return sqlPuzzle.queries.update.Update(table)


def delete():
    """
    Delete.
    """
    return sqlPuzzle.queries.delete.Delete()


def deleteFrom(table):
    """
    Delete.
    Param is table.
    """
    return sqlPuzzle.queries.delete.Delete().from_(table)


