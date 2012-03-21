# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#



class Object(object):
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, str(self))


