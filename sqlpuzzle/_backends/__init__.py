# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .mysql import MySqlBackend
from .postgresql import PostgreSqlBackend
from .sql import SqlBackend

__all__ = ('set_backend', 'get_backend',)


BACKEND = SqlBackend

BACKENDS = {
    'sql': SqlBackend,
    'mysql': MySqlBackend,
    'postgresql': PostgreSqlBackend,
    'sqlite': SqlBackend,
}


def set_backend(database):
    """
    Configure used database, so sqlpuzzle can generate queries which are needed.
    For now there is only support of MySQL and PostgreSQL.
    """
    new_backend = BACKENDS.get(database.lower())
    if not new_backend:
        raise Exception('Backend %s is not supported.' % database)
    global BACKEND
    BACKEND = new_backend


def get_backend():
    """
    Get backend which is used right now.
    """
    return BACKEND
