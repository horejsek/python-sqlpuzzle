# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

class NotSupprotedException(Exception):
    def __init__(self, method, typeOfQuery):
        self.method = method
        self.typeOfQuery = typeOfQuery
    
    def __str__(self):
        return "Method '%s' is not supported for type of query '%s'." % (
            self.method,
            self.typeOfQuery,
        )


class ConfirmUpdateAllException(Exception):
    def __str__(self):
        return "Are you sure, that you want update all records?"


class ConfirmDeleteAllException(Exception):
    def __str__(self):
        return "Are you sure, that you want delete all records?"


class ArgsParserException(Exception):
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return self.msg

