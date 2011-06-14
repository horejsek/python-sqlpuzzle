# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.queries
import datetime
import re


def addBackQuotes(value):
    """
    Add quotes.
    "table" => "`table`"
    "table.column" => "`table`.`column`"
    "table.col.umn" => "`table`.`col`.`umn`"
    "table.`col.umn`" => "`table`.`col.umn`"
    "`table`.`col.umn`" => "`table`.`col.umn`"
    """
    if isinstance(value, sqlPuzzle.queries.select.Select):
        return __subselect(value)
    return '.'.join('`%s`' % i for i in re.split('`([^`]+)`|\.', value) if i)


def sqlValue(value):
    """
    Wrap value.
    """
    if isinstance(value, (str, unicode)):
        return '"%s"' % value
    elif isinstance(value, (int, long)):
        return '%d' % value
    elif isinstance(value, float):
        return '%.5f' % value
    elif isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    elif isinstance(value, (list, tuple)):
        return "(%s)" % ", ".join(sqlValue(item) for item in value)
    elif isinstance(value, sqlPuzzle.queries.select.Select):
        return __subselect(value)
    elif value is None:
        return 'NULL'
    return 'undefined'


def __subselect(value):
    """
    Wrap value as subselect.
    """
    return "(%s)" % value

