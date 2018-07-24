from sqlpuzzle.exceptions import ConfirmUpdateAllException
from sqlpuzzle._queries.options import Options
from sqlpuzzle._queryparts import Tables, Values, Where
from .query import Query

__all__ = ('Update',)


class UpdateOptions(Options):
    _definition_of_options = {
        'ignore': {
            'off': '',
            'on': 'IGNORE',
        },
    }

    def ignore(self, allow=True):
        self._options['ignore'] = 'on' if allow else 'off'


class Update(Query):
    """
    Example:

    .. code-block:: python

        >>> sqlpuzzle.update('t').set(name='Alan', sallary=12345.67).where(id=1)
        <Update: UPDATE "t" SET "name" = 'Alan', "sallary" = 12345.67000 WHERE "id" = 1>
    """

    _queryparts = {
        'update_options': UpdateOptions,
        'tables': Tables,
        'values': Values,
        'where': Where,
    }
    _query_template = 'UPDATE%(update_options)s%(tables)s SET%(values)s%(where)s'

    def __init__(self, table=None):
        super().__init__()
        self._allow_update_all = False
        self.table(table)

    def __str__(self):
        if not self._where.is_set and not self._allow_update_all:
            raise ConfirmUpdateAllException()
        return super().__str__()

    def allow_update_all(self):
        """
        Allow query without ``WHERE`` condition.

        By default update without condition will raise exception
        :py:class:`ConfirmUpdateAllException <sqlpuzzle.exceptions.ConfirmUpdateAllException>`.
        If you want really update all rows without condition, allow it by calling
        this method.

        .. code-block:: python

            >>> sqlpuzzle.update('t')
            Traceback (most recent call last):
              ...
            ConfirmUpdateAllException: Are you sure, that you want update all records?
            >>> sqlpuzzle.update('t').set(a=1).allow_update_all()
            <Update: UPDATE "t" SET "a" = 1>
        """
        self._allow_update_all = True
        return self

    def forbid_update_all(self):
        """
        Forbid query without WHERE condition.

        By default update without condition will raise exception
        :py:class:`ConfirmUpdateAllException <sqlpuzzle.exceptions.ConfirmUpdateAllException>`.
        It can be allowed by calling method :py:meth:`~.allow_update_all`. If
        you want to again forbid it, call this method.
        """
        self._allow_update_all = False
        return self

    def table(self, table):
        self._tables.set(table)
        return self

    def set(self, *args, **kwds):
        self._values.set(*args, **kwds)
        return self

    def where(self, *args, **kwds):
        self._where.where(*args, **kwds)
        return self

    def join(self, table):
        self._tables.join(table)
        return self

    def inner_join(self, table):
        self._tables.inner_join(table)
        return self

    def left_join(self, table):
        self._tables.left_join(table)
        return self

    def right_join(self, table):
        self._tables.right_join(table)
        return self

    def on(self, *args, **kwds):
        self._tables.on(*args, **kwds)
        return self

    # UPDATE OPTIONS

    def ignore(self, allow=True):
        self._update_options.ignore(allow)
        return self
