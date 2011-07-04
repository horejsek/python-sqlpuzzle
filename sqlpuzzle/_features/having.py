# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle._features.conditions


class HavingCondition(sqlpuzzle._features.conditions.Condition):
    pass



class Having(sqlpuzzle._features.conditions.Conditions):
    def __init__(self):
        """Initialization of Having."""
        super(Having, self).__init__(HavingCondition)
    
    def __str__(self):
        """Print having (part of query)."""
        if self.isSet():
            return "HAVING %s" % " AND ".join(str(condition) for condition in self._conditions)
        return ""
    
    def __repr__(self):
        return "<Having: %s>" % self.__str__()

