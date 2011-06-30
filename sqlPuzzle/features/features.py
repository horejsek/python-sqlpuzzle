# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.customSql


class Features(object):
    def isCustumSql(self, *args, **kwds):
        return (
            kwds == {} and
            len(args) == 1 and
            isinstance(args[0], sqlPuzzle.customSql.CustomSql)
        )

