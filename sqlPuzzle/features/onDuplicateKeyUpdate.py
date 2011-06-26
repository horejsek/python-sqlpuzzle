# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import datetime

import sqlPuzzle.features.values



class OnDuplicateKeyUpdate(sqlPuzzle.features.values.Values):
    def __str__(self):
        """Print on duplicate key update."""
        return "ON DUPLICATE KEY UPDATE %s" % super(OnDuplicateKeyUpdate, self).__str__()

