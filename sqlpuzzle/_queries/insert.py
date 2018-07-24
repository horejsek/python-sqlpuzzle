from sqlpuzzle._backends import get_backend
from sqlpuzzle._queries.options import Options
from sqlpuzzle._queryparts import Tables, MultipleValues, OnDuplicateKeyUpdate, OnConflictDoUpdate
from .query import Query

__all__ = ('Insert',)


class InsertKeyword:
    def __init__(self):
        self._is_replace = False

    def __str__(self):
        if self._is_replace:
            return 'REPLACE'
        return 'INSERT'

    def __eq__(self, other):
        return type(self) == type(other) and self._is_replace == other._is_replace

    def replace(self):
        self._is_replace = True


class InsertOptions(Options):
    _definition_of_options = {
        'ignore': {
            'off': '',
            'on': 'IGNORE',
        },
    }

    def ignore(self, allow=True):
        self._options['ignore'] = 'on' if allow else 'off'


class Insert(Query):
    """
    Example:

    .. code-block:: python

        >>> sql = sqlpuzzle.insert_into('table')
        >>> sql.values(name='Alan', salary=12345.67)
        >>> sql.values(name='Bob', age=42)
        <Insert: INSERT INTO "table" ("age", "name", "salary") VALUES (NULL, 'Alan', 12345.67000), (42, 'Bob', NULL)>
    """

    _queryparts = {
        'keyword': InsertKeyword,
        'insert_options': InsertOptions,
        'tables': Tables,
        'values': MultipleValues,
        'on_duplicate_key_update': OnDuplicateKeyUpdate,
        'on_conflict_do_update': OnConflictDoUpdate,
    }
    _query_template = (
        '%(keyword)s%(insert_options)s INTO'
        '%(tables)s%(values)s%(on_duplicate_key_update)s%(on_conflict_do_update)s'
    )

    def into(self, table):
        self._tables.set(table)
        return self

    def values(self, *args, **kwds):
        self._values.add(*args, **kwds)
        return self

    def on_duplicate_key_update(self, *args, **kwds):
        backend = get_backend()
        if backend.supports_on_duplicate_key_update:
            self._on_duplicate_key_update.set(*args, **kwds)
        if backend.supports_on_conflict_do_update:
            self._on_conflict_do_update.set(*args, **kwds)
        if backend.supports_replace_into:
            if args or kwds:
                raise Exception(
                    'No argument for on_duplicate_key_update for backend {} is supported'.format(
                        backend.name
                    )
                )
            self._queryparts['keyword'].replace()
        return self

    # INSERT OPTIONS

    def ignore(self, allow=True):
        self._insert_options.ignore(allow)
        return self
