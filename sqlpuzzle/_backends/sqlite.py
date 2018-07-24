from .sql import SqlBackend

__all__ = ('SqliteBackend',)


class SqliteBackend(SqlBackend):
    name = 'SQLite'

    supports_replace_into = True
