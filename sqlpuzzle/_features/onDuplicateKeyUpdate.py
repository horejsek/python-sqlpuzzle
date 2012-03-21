# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

import sqlpuzzle._features.values



class OnDuplicateKeyUpdate(sqlpuzzle._features.values.Values):
    def __init__(self):
        super(OnDuplicateKeyUpdate, self).__init__()
        self._keywordOfFeature = 'ON DUPLICATE KEY UPDATE'

