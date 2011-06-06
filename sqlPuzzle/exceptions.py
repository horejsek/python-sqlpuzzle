# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

class SqlPuzzleException(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return "SqlPuzzleException: %s" % self.message


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

