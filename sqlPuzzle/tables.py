# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#
# This application is released under the GNU General Public License
# v3 (or, at your option, any later version). You can find the full
# text of the license under http://www.gnu.org/licenses/gpl.txt.
# By using, editing and/or distributing this software you agree to
# the terms and conditions of this license.
# Thank you for using free software!
#

class Tables:
    def __init__(self):
        """
        Initialization of Tables.
        """
        self.__tables = []
    
    def __str__(self):
        """
        Print tables (part of query).
        """
        return ", ".join("`%s`" % table for table in self.__tables)
    
    def isSet(self):
        """
        Is tables set?
        """
        return self.__tables != []
    
    def isSimple(self):
        """
        Is set only one table?
        """
        return len(self.__tables) == 1
    
    def set(self, tables):
        """
        Set tables.
        """
        if isinstance(tables, (tuple, list)):
            self.__tables = list(tables)
        elif isinstance(tables, (str, unicode)):
            self.__tables = [tables]

