from .conditions import Conditions

__all__ = ('Where',)


class Where(Conditions):
    _keyword_of_parts = 'WHERE'
