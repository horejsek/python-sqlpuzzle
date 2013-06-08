# -*- coding: utf-8 -*-


class Object(object):
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, str(self))
