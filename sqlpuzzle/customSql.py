# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#


class CustomSql(object):
    def __init__(self, string=''):
        self.__string = string
    
    def __str__(self):
        return self.__string

