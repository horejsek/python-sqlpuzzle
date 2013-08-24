# -*- coding: utf-8 -*-


class SqlPuzzleException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "SqlPuzzleException: %s" % self.message


class ConfirmException(SqlPuzzleException):
    def __init__(self):
        pass


class ConfirmUpdateAllException(ConfirmException):
    def __str__(self):
        return "Are you sure, that you want update all records?"


class ConfirmDeleteAllException(ConfirmException):
    def __str__(self):
        return "Are you sure, that you want delete all records?"


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
