# -*- coding: utf-8 -*-


class SqlPuzzleException(Exception):
    """
    Base exception. If you want to handle any exception of SQL puzzle in same
    way, catch this one.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "SqlPuzzleException: %s" % self.message


class ConfirmException(SqlPuzzleException):
    """
    Base confirm exception. If you want to handle any confirm exception
    (of update or delete) in same way, catch this one.
    """

    def __init__(self):
        pass


class ConfirmUpdateAllException(ConfirmException):
    """
    Raises when you want render update SQL without any where condition. It is
    security before changing all data by mistake.
    """

    def __str__(self):
        return "Are you sure, that you want update all records?"


class ConfirmDeleteAllException(ConfirmException):
    """
    Raises when you want render delete SQL without any where condition. It is
    security before droping all data by mistake.
    """

    def __str__(self):
        return "Are you sure, that you want delete all records?"


class InvalidArgumentException(SqlPuzzleException):
    """
    Raises when you pass invalid argument into SQL puzzle. For example instead
    of column reference some number and so.
    """

    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        if self.message:
            return "Invalid argument: %s" % self.message
        return "Invalid argument"


class InvalidQueryException(InvalidArgumentException):
    """
    Specific type of :py:class:`~.InvalidArgumentException`. Raises when you
    passed good arguments but final query does not make sense.
    """

    def __str__(self):
        if self.message:
            return "Invalid query: %s" % self.message
        return "Invalid query"
