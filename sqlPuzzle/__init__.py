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
    return sqlPuzzle.queries.select.Select(*columns)


def insert():
    return sqlPuzzle.queries.insert.Insert()


def insertInto(table):
    return sqlPuzzle.queries.insert.Insert().into(table)


def update(table):
    return sqlPuzzle.queries.update.Update(table)


def delete():
    return sqlPuzzle.queries.delete.Delete()


def deleteFrom(table):
    return sqlPuzzle.queries.delete.Delete().from_(table)


