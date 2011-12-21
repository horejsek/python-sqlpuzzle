# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle._libs.customSql
import sqlpuzzle._libs.sqlValue



class Count(sqlpuzzle._libs.customSql.CustomSql):
    def __init__(self, column=None):
        self._column = column

    def __str__(self):
        """Print custom SQL"""
        if not self._column or self._column == '*':
            return 'COUNT(*)'
        return 'COUNT(%s)' % sqlpuzzle._libs.sqlValue.SqlValue(self._column)

