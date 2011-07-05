# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle.customSql


class Features(object):
    def isCustumSql(self, args):
        return isinstance(args, sqlpuzzle.customSql.CustomSql)

