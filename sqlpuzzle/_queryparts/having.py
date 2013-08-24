# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .conditions import Condition, Conditions

__all__ = ('HavingCondition', 'Having')


class HavingCondition(Condition):
    pass


class Having(Conditions):
    _keyword_of_parts = 'HAVING'
    _separator_of_parts = ' AND '
