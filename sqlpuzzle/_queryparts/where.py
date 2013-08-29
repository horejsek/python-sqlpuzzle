# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .conditions import Conditions

__all__ = ('Where',)


class Where(Conditions):
    _keyword_of_parts = 'WHERE'
