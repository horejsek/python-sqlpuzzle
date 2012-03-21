# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

import types

import sqlpuzzle._libs.argsParser
import sqlpuzzle.exceptions


class Limit(sqlpuzzle._features.Feature):
    def __init__(self, limit=None, offset=None):
        """Initialization of Limit."""
        self._limit = limit
        self._offset = offset

    def _clear(self):
        """Clear object."""
        self._limit = None
        self._offset = None

    def __str__(self):
        """Print limit (part of query)."""
        limit = "LIMIT %s" % self._limit
        if self._offset is not None:
            limit = "%s OFFSET %s" % (limit, self._offset)
        return limit

    def __eq__(self, other):
        """Are limits equivalent?"""
        return (
            self._limit == other._limit and
            self._offset == other._offset
        )

    def isSet(self):
        """Is limit set?"""
        return self._limit is not None

    def limit(self, limit, offset=None):
        """Set LIMIT (and OFFSET)."""
        if not type(limit) in (int, long, types.NoneType):
            raise sqlpuzzle.exceptions.InvalidArgumentException()

        if limit is None:
            self._clear()
        else:
            self._limit = int(limit)
            if offset is not None:
                self.offset(offset)

        return self

    def offset(self, offset):
        """Set OFFSET."""
        if not type(offset) in (int, long, types.NoneType):
            raise sqlpuzzle.exceptions.InvalidArgumentException()

        self._offset = int(offset) if offset is not None else None

        return self
