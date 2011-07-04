# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import datetime

import sqlpuzzle.libs.argsParser
import sqlpuzzle.features.conditions


class WhereCondition(sqlpuzzle.features.conditions.Condition):
    pass



class Where(sqlpuzzle.features.conditions.Conditions):
    def __init__(self):
        """Initialization of Where."""
        super(Where, self).__init__(WhereCondition)
    
    def __str__(self):
        """Print where (part of query)."""
        if self.isSet():
            return "WHERE %s" % " AND ".join(str(condition) for condition in self._conditions)
        return ""
    
    def __repr__(self):
        return "<Where: %s>" % self.__str__()
