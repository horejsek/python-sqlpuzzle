# -*- coding: utf-8 -*-

import copy


class Object(object):
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, str(self))

    def copy(self):
        return copy.deepcopy(self)
