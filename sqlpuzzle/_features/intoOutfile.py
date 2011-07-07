# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle._libs.sqlValue
import sqlpuzzle.exceptions


class IntoOutfile(sqlpuzzle._features.Feature):
    def __init__(self):
        """Initialization of IntoOutfile."""
        self._intoOutfile = None
        self._fieldsTerminatedBy = None
        self._linesTerminatedBy = None
        self._optionallyEnclosedBy = None
    
    def __str__(self):
        """Print limit (part of query)."""
        intoOutfile = 'INTO OUTFILE "%s"' % self._intoOutfile
        if self._fieldsTerminatedBy is not None:
            intoOutfile = '%s FIELDS TERMINATED BY %s' % (intoOutfile, sqlpuzzle._libs.sqlValue.SqlValue(self._fieldsTerminatedBy))
        if self._linesTerminatedBy is not None:
            intoOutfile = '%s LINES TERMINATED BY %s' % (intoOutfile, sqlpuzzle._libs.sqlValue.SqlValue(self._linesTerminatedBy))
        if self._optionallyEnclosedBy is not None:
            intoOutfile = '%s OPTIONALLY ENCLOSED BY %s' % (intoOutfile, sqlpuzzle._libs.sqlValue.SqlValue(self._optionallyEnclosedBy))
        return intoOutfile
    
    def isSet(self):
        """Is intoOutfile set?"""
        return self._intoOutfile is not None
    
    def intoOutfile(self, intoOutfile):
        """Set INTO OUTFILE."""
        return self._setter('intoOutfile', intoOutfile)
    
    def fieldsTerminatedBy(self, fieldsTerminatedBy):
        """Set FIELDS TERMINATED BY."""
        return self._setter('fieldsTerminatedBy', fieldsTerminatedBy)
    
    def linesTerminatedBy(self, linesTerminatedBy):
        """Set LINES TERMINATED BY."""
        return self._setter('linesTerminatedBy', linesTerminatedBy)
    
    def optionallyEnclosedBy(self, optionallyEnclosedBy):
        """Set OPTIONALLY ENCLOSED BY."""
        return self._setter('optionallyEnclosedBy', optionallyEnclosedBy)
    
    def _setter(self, key, value):
        """Helper for seting options."""
        if not isinstance(value, (str, unicode)):
            raise sqlpuzzle.exceptions.InvalidArgumentException()
        setattr(self, '_%s' % key, value)
        return self

