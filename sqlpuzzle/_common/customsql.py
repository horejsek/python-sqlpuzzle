# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .object import Object
from .utils import force_text

__all__ = ('CustomSql',)


class CustomSql(Object):
    def __init__(self, string=''):
        """Custom SQL."""
        super(CustomSql, self).__init__()
        self._custom_sql_string = force_text(string)

    def __unicode__(self):
        return self._custom_sql_string
