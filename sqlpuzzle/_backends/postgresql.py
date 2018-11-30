from .sql import SqlBackend

__all__ = ('PostgreSqlBackend',)


class PostgreSqlBackend(SqlBackend):
    name = 'PostgreSQL'

    supports_full_join = True
    supports_on_conflict_do_update = True

    @classmethod
    def boolean(cls, value):
        return 'true' if value else 'false'

    @classmethod
    def bytes(cls, value):
        return "E'\\\\x{}'".format(value.hex())
