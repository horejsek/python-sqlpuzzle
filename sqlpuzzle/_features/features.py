# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle.customSql


class Features(object):
    def isCustumSql(self, *args, **kwds):
        return (
            kwds == {} and
            len(args) == 1 and
            isinstance(args[0], sqlpuzzle.customSql.CustomSql)
        )

