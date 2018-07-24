from sqlpuzzle._common import check_type_decorator
from .queryparts import QueryPart

__all__ = ('Limit',)


class Limit(QueryPart):
    def __init__(self, limit=None, offset=None):
        super(Limit, self).__init__()
        self._limit = limit
        self._offset = offset

    def __unicode__(self):
        res = ''
        if self._limit is not None:
            res += 'LIMIT {}'.format(self._limit)
        if self._offset is not None:
            if res:
                res += ' '
            res += 'OFFSET {}'.format(self._offset)
        return res

    def __eq__(self, other):
        return (
            type(self) == type(other) and
            self._limit == other._limit and
            self._offset == other._offset
        )

    @property
    def is_set(self):
        return self._limit is not None or self._offset is not None

    @check_type_decorator((type(None), int))
    def limit(self, limit, offset=None):
        if limit is None:
            self._limit = None
            self._offset = None
        else:
            self._limit = int(limit)
            if offset is not None:
                self.offset(offset)
        return self

    @check_type_decorator((type(None), int))
    def offset(self, offset):
        self._offset = int(offset) if offset else None
        return self
