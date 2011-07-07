# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import datetime

import sqlpuzzle._libs.argsParser
import sqlpuzzle._features.conditions


class WhereCondition(sqlpuzzle._features.conditions.Condition):
    pass



class Where(sqlpuzzle._features.conditions.Conditions):
    def __init__(self):
        """Initialization of Where."""
        super(Where, self).__init__(WhereCondition)
        self._keywordOfFeature = 'WHERE'
        self._separatorOfFeatures = ' AND '
