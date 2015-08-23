# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six

from .sql import SqlBackend

__all__ = ('PostgreSqlBackend',)


class PostgreSqlBackend(SqlBackend):
    name = 'PostgreSQL'

    supports_full_join = True

    @classmethod
    def boolean(cls, value):
        return six.u('true') if value else six.u('false')
