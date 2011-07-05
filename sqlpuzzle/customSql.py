# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#


class CustomSql(object):
    def __init__(self, string=''):
        """Initialization of CustomSql"""
        self.__string = string
    
    def __str__(self):
        """Print custom SQL"""
        return self.__string
    
    def __getattr__(self, attr):
        """Fake method for camparison"""
        return None

