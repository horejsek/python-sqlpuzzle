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

print sql1 & sql2
# output: SELECT * FROM `t1` UNION ALL SELECT * FROM `t2`

print sql1 | sql2
# output: SELECT * FROM `t1` UNION SELECT * FROM `t2`

print sql1 & sql2 | sql1
# output: SELECT * FROM `t1` UNION ALL SELECT * FROM `t2` UNION SELECT * FROM `t1`

print sqlPuzzle.select(sql1 | sql2).from_('t')
# output: SELECT (SELECT * FROM `t1` UNION SELECT * FROM `t2`) FROM `t`

print sqlPuzzle.selectFrom(sql1 & sql2)
# output: SELECT * FROM (SELECT * FROM `t1` UNION ALL SELECT * FROM `t2`)
