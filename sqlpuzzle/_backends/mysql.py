# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .sql import SqlBackend

__all__ = ('MySqlBackend',)


class MySqlBackend(SqlBackend):
    name = 'MySQL'

    reference_quote = '`'
    supports_on_duplicate_key_update = True
