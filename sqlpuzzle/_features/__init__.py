# -*- coding: utf-8 -*-

import inspect

import sqlpuzzle._libs.object
import sqlpuzzle.exceptions


class Feature(sqlpuzzle._libs.object.Object):
    def copy(self):
        """Create copy."""
        args = inspect.getargspec(self.__class__.__init__)[0][1:]
        new_args = [getattr(self, '_%s' % arg.strip('_')) for arg in args]
        new_feature = self.__class__(*new_args)
        return new_feature

    def is_set(self):
        """Is feature set?"""
        return True


class Features(sqlpuzzle._libs.object.Object):
    def __init__(self):
        """Initialization of Features."""
        super(Features, self).__init__()
        self._features = ListOfFeatures()
        self._separator_of_features = ', '
        self._keyword_of_feature = ''
        self._default_query_string = ''

    def copy(self):
        """Create copy of features."""
        new_features = self.__class__()
        new_features._features = self._features.copy()
        return new_features

    def __str__(self):
        """Print features."""
        if self.is_set():
            self._features.set_separator(self._separator_of_features)
            if self._keyword_of_feature:
                return '%s %s' % (self._keyword_of_feature, str(self._features))
            return str(self._features)
        return self._default_query_string

    def __contains__(self, other_feature):
        """Is item (column) in columns?"""
        for feature in self._features:
            if feature == other_feature:
                return True
        return False

    def __eq__(self, other):
        """Are objects of features equivalent?"""
        if not isinstance(other, Features) or len(self._features) != len(other._features):
            return False
        return all(bool(sf == of) for sf, of in zip(self._features, other._features))

    def is_set(self):
        """Is feature set?"""
        return self._features != []

    def append_feature(self, feature):
        """Append feature into list of features."""
        self._features.append(feature)

    def is_custum_sql(self, args):
        """Is custom sql?"""
        return isinstance(args, sqlpuzzle._libs.customsql.CustomSql)


class ListOfFeatures(list):
    def copy(self):
        """Create copy of list of features."""
        new_list_of_features = self.__class__()
        for feature in self:
            new_list_of_features.append(feature.copy())
        return new_list_of_features

    def append(self, feature):
        if not isinstance(feature, (Feature, Features)):
            raise sqlpuzzle.exceptions.SqlPuzzleError(
                'Appended item must be instance of Feature.')
        super(ListOfFeatures, self).append(feature)

    def set_separator(self, separator):
        self._separator = separator

    def __str__(self):
        return self._separator.join(str(f) for f in self)
