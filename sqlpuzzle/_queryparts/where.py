from sqlpuzzle._common import Object
from .conditions import Conditions

__all__ = ('Where', 'Exists')


class Where(Conditions):
    _keyword_of_parts = 'WHERE'


class Exists(Object):
    def __init__(self, subquery):
        super().__init__()
        self._subquery = subquery

    def __str__(self):
        return 'EXISTS({})'.format(self._subquery)
