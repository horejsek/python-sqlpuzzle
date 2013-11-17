# -*- coding: utf-8 -*-

import six

from sqlpuzzle._common import Object, force_text

__all__ = ('Query',)


class Query(Object):
    _queryparts = {}
    _query_template = ''

    def __init__(self):
        super(Query, self).__init__()
        self._queryparts = dict([(key, cls()) for key, cls in six.iteritems(self._queryparts)])
        for key, querypart in six.iteritems(self._queryparts):
            setattr(self, '_%s' % key, querypart)

    def __unicode__(self):
        context = {}
        for key, querypart in six.iteritems(self._queryparts):
            is_set = getattr(querypart, 'is_set', lambda: True)()
            if is_set:
                context[key] = ' ' + force_text(querypart)
            else:
                context[key] = ''
        return self._query_template % context

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        sqps = self._queryparts
        oqps = other._queryparts
        if len(sqps) != len(oqps):
            return False
        return all(bool(sqp == oqp) for sqp, oqp in zip(sqps.values(), oqps.values()))

    def __hash__(self):
        """
        Provides hash, so query instance can be used in dictionary key.
        This functionality is required for example in joins.
        """
        return id(self)

    def has(self, querypart_name, value=None):
        """Returns True if `querypart_name` with `value` is set.

        For example you can check if you already used condition by `sql.has('where')`.

        If you want to check for more information, for example if that condition
        also contain ID, you can do this by `sql.has('where', 'id')`.
        """
        querypart = self._queryparts.get(querypart_name)
        if not querypart:
            return False
        if not querypart.is_set():
            return False
        if value:
            return querypart.has(value)
        return True
