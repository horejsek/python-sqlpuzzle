# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

import sqlpuzzle._features.conditions


class HavingCondition(sqlpuzzle._features.conditions.Condition):
    pass



class Having(sqlpuzzle._features.conditions.Conditions):
    def __init__(self):
        """Initialization of Having."""
        super(Having, self).__init__(HavingCondition)
        self._keywordOfFeature = 'HAVING'
        self._separatorOfFeatures = ' AND '

