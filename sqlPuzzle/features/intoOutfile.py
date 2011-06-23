# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.exceptions


class IntoOutfile(object):
    def __init__(self):
        """
        Initialization of IntoOutfile.
        """
        self._intoOutfile = None
        self._fieldsTerminatedBy = None
        self._linesTerminatedBy = None
        self._optionallyEnclosedBy = None
    
    def __str__(self):
        """
        Print limit (part of query).
        """
        intoOutfile = 'INTO OUTFILE "%s"' % self._intoOutfile
        if self._fieldsTerminatedBy is not None:
            intoOutfile = '%s FIELDS TERMINATED BY %s' % (intoOutfile, self._wrapValue(self._fieldsTerminatedBy))
        if self._linesTerminatedBy is not None:
            intoOutfile = '%s LINES TERMINATED BY %s' % (intoOutfile, self._wrapValue(self._linesTerminatedBy))
        if self._optionallyEnclosedBy is not None:
            intoOutfile = '%s OPTIONALLY ENCLOSED BY %s' % (intoOutfile, self._wrapValue(self._optionallyEnclosedBy))
        return intoOutfile
    
    def __repr__(self):
        return "<IntoOutfile: %s>" % self.__str__()
    
    def _wrapValue(self, value):
        if value == '"':
            return "'%s'" % value
        return '"%s"' % value
    
    def isSet(self):
        """
        Is intoOutfile set?
        """
        return self._intoOutfile is not None
    
    def intoOutfile(self, intoOutfile):
        """
        Set INTO OUTFILE.
        """
        if not isinstance(intoOutfile, (str, unicode)):
            raise sqlPuzzle.exceptions.InvalidArgumentException()
        self._intoOutfile = intoOutfile
        return self
    
    def fieldsTerminatedBy(self, fieldsTerminatedBy):
        """
        Set FIELDS TERMINATED BY.
        """
        if not isinstance(fieldsTerminatedBy, (str, unicode)):
            raise sqlPuzzle.exceptions.InvalidArgumentException()
        self._fieldsTerminatedBy = fieldsTerminatedBy
        return self
    
    def linesTerminatedBy(self, linesTerminatedBy):
        """
        Set LINES TERMINATED BY.
        """
        if not isinstance(linesTerminatedBy, (str, unicode)):
            raise sqlPuzzle.exceptions.InvalidArgumentException()
        self._linesTerminatedBy = linesTerminatedBy
        return self
    
    def optionallyEnclosedBy(self, optionallyEnclosedBy):
        """
        Set OPTIONALLY ENCLOSED BY.
        """
        if not isinstance(optionallyEnclosedBy, (str, unicode)):
            raise sqlPuzzle.exceptions.InvalidArgumentException()
        self._optionallyEnclosedBy = optionallyEnclosedBy
        return self

