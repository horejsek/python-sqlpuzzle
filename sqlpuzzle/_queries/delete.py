from __future__ import absolute_import

from sqlpuzzle.exceptions import ConfirmDeleteAllException
from sqlpuzzle._queries.options import Options
from sqlpuzzle._queryparts import Tables, Where
from .query import Query

__all__ = ('Delete',)


class DeleteOptions(Options):
    _definition_of_options = {
        'ignore': {
            'off': '',
            'on': 'IGNORE',
        },
    }

    def ignore(self, allow=True):
        self._options['ignore'] = 'on' if allow else 'off'


class Delete(Query):
    """
    Example:

    .. code-block:: python

        >>> sqlpuzzle.delete_from('t').where(id=1)
        <Delete: DELETE FROM "t" WHERE "id" = 1>
    """

    _queryparts = {
        'delete_options': DeleteOptions,
        'tables': Tables,
        'references': Tables,
        'where': Where,
    }
    _query_template = 'DELETE%(delete_options)s%(tables)s FROM%(references)s%(where)s'

    def __init__(self, *tables):
        super(Delete, self).__init__()
        self._allow_delete_all = False
        self._tables.set(*tables)

    def __unicode__(self):
        if not self._where.is_set and not self._allow_delete_all:
            raise ConfirmDeleteAllException()
        return super(Delete, self).__unicode__()

    def allow_delete_all(self):
        """
        Allow query without ``WHERE`` condition.

        By default delete without condition will raise exception
        :py:class:`ConfirmDeleteAllException <sqlpuzzle.exceptions.ConfirmDeleteAllException>`.
        If you want really delete all rows without condition, allow it by calling
        this method.

        .. code-block:: python

            >>> sqlpuzzle.delete_from('t')
            Traceback (most recent call last):
              ...
            ConfirmDeleteAllException: Are you sure, that you want delete all records?
            >>> sqlpuzzle.delete_from('t').allow_delete_all()
            <Delete: DELETE FROM "t">
        """
        self._allow_delete_all = True
        return self

    def forbid_delete_all(self):
        """
        Forbid query without WHERE condition.

        By default delete without condition will raise exception
        :py:class:`ConfirmDeleteAllException <sqlpuzzle.exceptions.ConfirmDeleteAllException>`.
        It can be allowed by calling method :py:meth:`~.allow_delete_all`. If
        you want to again forbid it, call this method.
        """
        self._allow_delete_all = False
        return self

    def delete(self, *tables):
        self._tables.set(*tables)
        return self

    def from_(self, *args, **kwds):
        self._references.set(*args, **kwds)
        return self

    def from_table(self, table, alias=None):
        self._references.set((table, alias))
        return self

    def from_tables(self, *args, **kwds):
        self.from_(*args, **kwds)
        return self

    def join(self, table):
        self._references.join(table)
        return self

    def inner_join(self, table):
        self._references.inner_join(table)
        return self

    def left_join(self, table):
        self._references.left_join(table)
        return self

    def right_join(self, table):
        self._references.right_join(table)
        return self

    def on(self, *args, **kwds):
        self._references.on(*args, **kwds)
        return self

    def where(self, *args, **kwds):
        self._where.where(*args, **kwds)
        return self

    # DELETE OPTIONS

    def ignore(self, allow=True):
        self._delete_options.ignore(allow)
        return self
