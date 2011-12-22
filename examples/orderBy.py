#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle

sql = sqlpuzzle.selectFrom('table')

sql.orderBy('name')
print sql
# output: SELECT * FROM `table` ORDER BY `name`

sql.orderBy(('name', 'desc'), 'id')
print sql
# output: SELECT * FROM `table` ORDER BY `name` DESC, `id`

sql.orderBy(('name', 'asc')) # or only 'name'
print sql
# output: SELECT * FROM `table` ORDER BY `name`, `id`

# same as before:
sql.orderBy({'name': 'asc'}) # dict looks better
sql.orderBy(name='asc') # also possible
