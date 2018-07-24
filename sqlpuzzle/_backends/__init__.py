from .mysql import MySqlBackend
from .postgresql import PostgreSqlBackend
from .sql import SqlBackend
from .sqlite import SqliteBackend

__all__ = ('set_backend', 'get_backend',)


BACKEND = SqlBackend

BACKENDS = {
    'sql': SqlBackend,
    'mysql': MySqlBackend,
    'postgresql': PostgreSqlBackend,
    'sqlite': SqliteBackend,
}


def set_backend(database):
    """
    Configure used database, so sqlpuzzle can generate queries which are needed.
    For now there is only support of MySQL and PostgreSQL.
    """
    new_backend = BACKENDS.get(database.lower())
    if not new_backend:
        raise Exception('Backend {} is not supported.'.format(database))
    global BACKEND  # pylint: disable=global-statement
    BACKEND = new_backend


def get_backend():
    """
    Get backend which is used right now.
    """
    return BACKEND
