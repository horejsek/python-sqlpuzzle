# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#
# This application is released under the GNU General Public License
# v3 (or, at your option, any later version). You can find the full
# text of the license under http://www.gnu.org/licenses/gpl.txt.
# By using, editing and/or distributing this software you agree to
# the terms and conditions of this license.
# Thank you for using free software!
#

EQ = EQUAL_TO = 1
NE = NOT_EQUAL_TO = 2

GT = GRATHER_THAN = 3
GE = GRATHER_THAN_OR_EQUAL_TO = 4

LT = LESS_THAN = 5
LE = LESS_TAHN_OR_EQUAL_TO = 6

LIKE = 7


RELATIONS = {
    EQ: '=',
    NE: '!=',
    GT: '>',
    GE: '>=',
    LT: '<',
    LE: '<=',
    LIKE: 'LIKE',
}


class Condition:
    def __init__(self):
        """
        Initialization of Condition.
        """
        self.__column = None
        self.__value = None
        self.__relation = None
    
    def __str__(self):
        """
        Print condition (part of WHERE).
        """
        if isinstance(self.__value, int):
            formatString = '`%s` %s %s'
        else:
            formatString = '`%s` %s "%s"'
            
        return formatString % (
            self.__column,
            RELATIONS[self.__relation],
            self.__value,
        )
    
    def set(self, column, value, relation=None):
        """
        Set column, value and relation.
        """
        self.setColumn(column)
        self.setValue(value)
        self.setRelation(relation or EQ)
    
    def setColumn(self, column):
        """
        Set column.
        """
        self.__column = column
    
    def setValue(self, value):
        """
        Set value.
        """
        self.__value = value
    
    def setRelation(self, relation):
        """
        Set relation.
        """
        self.__relation = relation


class Conditions:
    def __init__(self):
        """
        Initialization of Conditions.
        """
        self.__conditions = []
    
    def __str__(self):
        """
        Print limit (part of query).
        """
        return "WHERE %s" % " AND ".join(str(condition) for condition in self.__conditions)
    
    def isSet(self):
        """
        Is where set?
        """
        return self.__conditions != []
    
    def where(self, *args, **kwargs):
        """
        Set condition(s).
        """
        list_ = None
        dict_ = None
        
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            list_ = args[0]
        elif len(args) == 1 and isinstance(args[0], dict):
            dict_ = args[0]
        elif 2 <= len(args) <= 3:
            list_ = (args,)
        elif kwargs is not None:
            dict_ = kwargs
        
        if list_ is not None:
            for c in list_:
                condition = Condition()
                condition.set(c[0], c[1])
                if len(c) == 3:
                    condition.setRelation(c[2])
                self.__conditions.append(condition)
        elif dict_ is not None:
            for c, v in dict_.iteritems():
                condition = Condition()
                condition.set(c, v)
                self.__conditions.append(condition)

