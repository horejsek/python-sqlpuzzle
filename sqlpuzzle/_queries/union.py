from sqlpuzzle.exceptions import InvalidArgumentException
from sqlpuzzle._common import check_type_decorator
from .query import Query

__all__ = ('UNION', 'UNION_ALL', 'Union')


UNION = 'UNION'
UNION_ALL = 'UNION ALL'
UNION_TYPES = (UNION, UNION_ALL)


class Union(Query):
    """
    Class representing ``UNION`` or ``UNION ALL``.

    You will get it by calling magic methods on :py:class:`Select <sqlpuzzle._queries.select.Select>`:

    .. code-block:: python

        >>> sqlpuzzle.select('t') & sqlpuzzle.select('u')
        <Union: SELECT "t" UNION ALL SELECT "u">
        >>> sqlpuzzle.select('t') | sqlpuzzle.select('u')
        <Union: SELECT "t" UNION SELECT "u">
    """

    def __init__(self, query1, query2, union_type=UNION):
        super(Union, self).__init__()
        self.query1 = query1
        self.query2 = query2
        self.union_type = union_type

    def __unicode__(self):
        return '%s %s %s' % (
            self.query1,
            self.union_type,
            self.query2,
        )

    def __eq__(self, other):
        return (
            type(self) == type(other) and
            self.query1 == other.query1 and
            self.query2 == other.query2 and
            self.union_type == other.union_type
        )

    def __and__(self, other):
        """
        Returns :py:class:`sqlpuzzle._queries.union.Union` instance, ``UNION ALL``.

        .. code-block:: python

            >>> sqlpuzzle.select('t') & sqlpuzzle.select('u') & sqlpuzzle.select('v')
            <Union: SELECT "t" UNION ALL SELECT "u" UNION ALL SELECT "v">
        """
        return Union(self, other, UNION_ALL)

    def __or__(self, other):
        """
        Returns :py:class:`sqlpuzzle._queries.union.Union` instance, ``UNION``.

        .. code-block:: python

            >>> sqlpuzzle.select('t') | sqlpuzzle.select('u') | sqlpuzzle.select('v')
            <Union: SELECT "t" UNION SELECT "u" UNION SELECT "v">
        """
        return Union(self, other, UNION)

    @property
    def query1(self):
        return self._query1

    @query1.setter
    @check_type_decorator()
    def query1(self, query):
        self._query1 = query

    @property
    def query2(self):
        return self._query2

    @query2.setter
    @check_type_decorator()
    def query2(self, query):
        self._query2 = query

    @property
    def union_type(self):
        return self._union_type

    @union_type.setter
    @check_type_decorator(str)
    def union_type(self, union_type):
        if not union_type in UNION_TYPES:
            raise InvalidArgumentException('Union type can not be %s.' % union_type)
        self._union_type = union_type
