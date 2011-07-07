# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle._libs.object
import sqlpuzzle.exceptions



class Feature(sqlpuzzle._libs.object.Object):
    def isSet(self):
        """Is feature set?"""
        return True



class Features(sqlpuzzle._libs.object.Object):
    def __init__(self):
        """Initialization of Features."""
        self._features = ListOfFeatures()
        self._separatorOfFeatures = ', '
        self._keywordOfFeature = ''
        self._defaultQueryString = ''
    
    def __str__(self):
        """Print features."""
        if self.isSet():
            self._features.setSeparator(self._separatorOfFeatures)
            if self._keywordOfFeature:
                return '%s %s' % (self._keywordOfFeature, str(self._features))
            return str(self._features)
        return self._defaultQueryString
    
    def __contains__(self, otherFeature):
        """Is item (column) in columns?"""
        for feature in self._features:
            if feature == otherFeature:
                return True
        return False

    def __eq__(self, other):
        """Are objects of features equivalent?"""
        if not isinstance(other, Features):
            return False
        return all(bool(sf == of) for sf, of in zip(self._features, other._features))
    
    def isSet(self):
        """Is feature set?"""
        return self._features != []
    
    def isCustumSql(self, args):
        """Is custom sql?"""
        return isinstance(args, sqlpuzzle.customSql.CustomSql)



class ListOfFeatures(list):
    def append(self, feature):
        if not isinstance(feature, Feature):
            raise sqlpuzzle.exceptions.SqlPuzzleError('Appended item must be instance of Feature.')
        super(ListOfFeatures, self).append(feature)
    
    def setSeparator(self, separator):
        self._separator = separator
    
    def __str__(self):
        return self._separator.join(str(f) for f in self)

