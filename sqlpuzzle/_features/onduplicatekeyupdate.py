# -*- coding: utf-8 -*-

import sqlpuzzle._features.values


class OnDuplicateKeyUpdate(sqlpuzzle._features.values.Values):
    def __init__(self):
        super(OnDuplicateKeyUpdate, self).__init__()
        self._keyword_of_feature = 'ON DUPLICATE KEY UPDATE'
