# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .values import Values

__all__ = ('OnDuplicateKeyUpdate',)


class OnDuplicateKeyUpdate(Values):
    _keyword_of_parts = 'ON DUPLICATE KEY UPDATE'
