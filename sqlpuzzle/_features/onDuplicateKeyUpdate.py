# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import datetime

import sqlpuzzle._features.values



class OnDuplicateKeyUpdate(sqlpuzzle._features.values.Values):
    def __str__(self):
        """Print on duplicate key update."""
        return "ON DUPLICATE KEY UPDATE %s" % super(OnDuplicateKeyUpdate, self).__str__()

