#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle

sql1 = sqlPuzzle.selectFrom('t1')
sql2 = sqlPuzzle.selectFrom('t2')

print sql1 & sql2 # returning string, not instance!
# output: SELECT * FROM `t1` UNION ALL SELECT * FROM `t2`

print sql1 | sql2 # returning string, not instance!
# output: SELECT * FROM `t1` UNION SELECT * FROM `t2`
