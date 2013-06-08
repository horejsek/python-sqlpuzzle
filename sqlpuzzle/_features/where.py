# -*- coding: utf-8 -*-

import sqlpuzzle._libs.argsparser
import sqlpuzzle._features.conditions


class WhereCondition(sqlpuzzle._features.conditions.Condition):
    pass


class Where(sqlpuzzle._features.conditions.Conditions):
    def __init__(self):
        """Initialization of Where."""
        super(Where, self).__init__(WhereCondition)
        self._keyword_of_feature = 'WHERE'
        self._separator_of_features = ' AND '
