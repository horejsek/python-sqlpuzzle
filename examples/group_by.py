#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlpuzzle


sql = sqlpuzzle.select_from('table')

sql.group_by('name')
print(sql)
# output: SELECT * FROM `table` GROUP BY `name`

sql.group_by(('name', 'desc'), 'id')
print(sql)
# output: SELECT * FROM `table` GROUP BY `name` DESC, `id`

sql.group_by(('name', 'asc'))  # or only 'name'
print(sql)
# output: SELECT * FROM `table` GROUP BY `name`, `id`

# Same as before:
sql.group_by({'name': 'asc'})  # dict looks better
sql.group_by(name='asc')  # also possible
