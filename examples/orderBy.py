#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle

sql = sqlPuzzle.selectFrom('table')
sql.orderBy('name')
print sql
# output: SELECT * FROM `table` ORDER BY `name`

sql.orderBy(('name', 'desc'), 'id')
print sql
# output: SELECT * FROM `table` ORDER BY `name` DESC, `id`

sql.orderBy(('name', 'asc')) # or only 'name'
print sql
# output: SELECT * FROM `table` ORDER BY `name`, `id`
