#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle

sql1 = sqlpuzzle.selectFrom('t1')
sql2 = sqlpuzzle.selectFrom('t2')

print sql1 & sql2
# output: SELECT * FROM `t1` UNION ALL SELECT * FROM `t2`

print sql1 | sql2
# output: SELECT * FROM `t1` UNION SELECT * FROM `t2`

print sql1 & sql2 | sql1
# output: SELECT * FROM `t1` UNION ALL SELECT * FROM `t2` UNION SELECT * FROM `t1`

print sqlpuzzle.select(sql1 | sql2).from_('t')
# output: SELECT (SELECT * FROM `t1` UNION SELECT * FROM `t2`) FROM `t`

print sqlpuzzle.selectFrom(sql1 & sql2)
# output: SELECT * FROM (SELECT * FROM `t1` UNION ALL SELECT * FROM `t2`)
