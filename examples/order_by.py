#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlpuzzle


sql = sqlpuzzle.select_from('table')

sql.order_by('name')
print(sql)
# output: SELECT * FROM `table` ORDER BY `name`

sql.order_by(('name', 'desc'), 'id')
print(sql)
# output: SELECT * FROM `table` ORDER BY `name` DESC, `id`

sql.order_by(('name', 'asc'))  # or only 'name'
print(sql)
# output: SELECT * FROM `table` ORDER BY `name`, `id`

# same as before:
sql.order_by({'name': 'asc'})  # dict looks better
sql.order_by(name='asc')  # also possible
