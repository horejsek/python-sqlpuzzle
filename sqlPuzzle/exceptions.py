# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

#### Main exceptions


class SqlPuzzleException(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return "SqlPuzzleException: %s" % self.message


class SqlPuzzleError(SqlPuzzleException):
    def __str__(self):
        return "SqlPuzzleError: %s" % self.message


class SqlPuzzleNotImplemeted(SqlPuzzleException):
    def __str__(self):
        return "SqlPuzzleNotImplemeted: %s" % self.message

#### Confirms


class ConfirmException(SqlPuzzleException):
    def __init__(self):
        pass


class ConfirmUpdateAllException(ConfirmException):
    def __str__(self):
        return "Are you sure, that you want update all records?"


class ConfirmDeleteAllException(ConfirmException):
    def __str__(self):
        return "Are you sure, that you want delete all records?"


#### Wrong input


class InvalidArgumentException(SqlPuzzleException):
    def __init__(self, message=''):
        self.message = message
    
    def __str__(self):
        if self.message:
            return "Invalid argument: %s" % self.message
        return "Invalid argument"


class InvalidQueryException(InvalidArgumentException):
    def __str__(self):
        if self.message:
            return "Invalid query: %s" % self.message
        return "Invalid query"


class NotSupprotedException(SqlPuzzleException):
    def __init__(self, method, typeOfQuery):
        self.method = method
        self.typeOfQuery = typeOfQuery
    
    def __str__(self):
        return "Method '%s' is not supported for type of query '%s'." % (
            self.method,
            self.typeOfQuery,
        )




