#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle

sql = sqlpuzzle.selectFrom('table')
sql.groupBy('name')
print sql
# output: SELECT * FROM `table` GROUP BY `name`

sql.groupBy(('name', 'desc'), 'id')
print sql
# output: SELECT * FROM `table` GROUP BY `name` DESC, `id`

sql.groupBy(('name', 'asc')) # or only 'name'
print sql
# output: SELECT * FROM `table` GROUP BY `name`, `id`
