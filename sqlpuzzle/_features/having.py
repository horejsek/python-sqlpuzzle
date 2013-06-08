# -*- coding: utf-8 -*-

import sqlpuzzle._features.conditions


class HavingCondition(sqlpuzzle._features.conditions.Condition):
    pass


class Having(sqlpuzzle._features.conditions.Conditions):
    def __init__(self):
        """Initialization of Having."""
        super(Having, self).__init__(HavingCondition)
        self._keyword_of_feature = 'HAVING'
        self._separator_of_features = ' AND '
