# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .conditions import Condition, Conditions

__all__ = ('WhereCondition', 'Where')


class WhereCondition(Condition):
    pass


class Where(Conditions):
    _keyword_of_parts = 'WHERE'
    _separator_of_parts = ' AND '
