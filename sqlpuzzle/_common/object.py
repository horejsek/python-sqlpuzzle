# -*- coding: utf-8 -*-

import six

import copy

__all__ = ('Object',)


class Object(object):
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, str(self))

    def __str__(self):
        if six.PY3:
            return self.__unicode__()
        return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        return six.u('<Object>')

    def tosql(self):
        if six.PY3:
            return self.__str__()
        return self.__unicode__()

    def copy(self):
        return copy.deepcopy(self)
