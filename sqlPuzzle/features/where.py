# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import datetime

import sqlPuzzle.libs.argsParser
import sqlPuzzle.features.conditions


class WhereCondition(sqlPuzzle.features.conditions.Condition):
    pass



class Where(sqlPuzzle.features.conditions.Conditions):
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
