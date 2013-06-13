# -*- coding: utf-8 -*-

import sqlpuzzle._libs.object
import sqlpuzzle.exceptions


class Query(sqlpuzzle._libs.object.Object):
    def __init__(self):
        """Initialization of Query."""
        super(Query, self).__init__()
        self.__features = {}
        self.__keys_of_features_for_auto_printing = ()

    def __hash__(self):
        return id(self)

    def __str__(self):
        """Print query."""
        return "Abstract Query object"

    def __eq__(self, other):
        """Are queries equivalent?"""
        if self.__class__ != other.__class__:
            return False
        sfs = self._get_features()
        ofs = other._get_features()
        if len(sfs) != len(ofs):
            return False
        return all(bool(sf == of) for sf, of in zip(sfs.values(), ofs.values()))

    def _print_features(self, prefix=''):
        """Append features into query."""
        query = str(prefix)
        for key_of_feature in self.__keys_of_features_for_auto_printing:
            object_ = self._get_feature(key_of_feature)
            if object_.is_set():
                query = '%s %s' % (query, object_)
        return query

    def _set_features(self, **kwds):
        """Set features."""
        self.__features = kwds

    def _set_keys_of_features_for_auto_printing(self, *args):
        """Set features which is proposed to automatic print."""
        self.__keys_of_features_for_auto_printing = args

    def _get_features(self):
        """Get features."""
        return dict(self.__features)

    def _get_feature(self, key_of_feature):
        """Get feature."""
        if key_of_feature in self.__features:
            return self.__features[key_of_feature]
        raise sqlpuzzle.exceptions.NotSupprotedException(key_of_feature, self.__class__.__name__)

    @property
    def _tables(self):
        return self._get_feature('tables')

    @property
    def _references(self):
        return self._get_feature('references')

    @property
    def _columns(self):
        return self._get_feature('columns')

    @property
    def _values(self):
        return self._get_feature('values')

    @property
    def _on_duplicate_key_update(self):
        return self._get_feature('on_duplicate_key_update')

    @property
    def _where(self):
        return self._get_feature('where')

    @property
    def _group_by(self):
        return self._get_feature('group_by')

    @property
    def _having(self):
        return self._get_feature('having')

    @property
    def _order_by(self):
        return self._get_feature('order_by')

    @property
    def _limit(self):
        return self._get_feature('limit')

    @property
    def _into_outfile(self):
        return self._get_feature('into_outfile')

    @property
    def _select_options(self):
        return self._get_feature('select_options')
