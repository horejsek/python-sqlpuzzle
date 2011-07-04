# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import datetime

import sqlpuzzle.features.values



class OnDuplicateKeyUpdate(sqlpuzzle.features.values.Values):
    def __str__(self):
        """Print on duplicate key update."""
        return "ON DUPLICATE KEY UPDATE %s" % super(OnDuplicateKeyUpdate, self).__str__()

