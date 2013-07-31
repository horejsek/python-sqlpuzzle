# -*- coding: utf-8 -*-

import sqlpuzzle._features


class CustomSql(sqlpuzzle._features.Feature):
    def __init__(self, string=''):
        """Initialization of CustomSql"""
        super(CustomSql, self).__init__()
        self._custom_sql_string = string

    def __str__(self):
        """Print custom SQL"""
        return self._custom_sql_string

