#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle

#---- BASE ---------------------------------------------------------------------

print sqlPuzzle.select().from_('table')
# output: SELECT * FROM `table`

print sqlPuzzle.selectFrom('table')
# same output as previous command

#---- COLUMNS & TABLES ---------------------------------------------------------

sql = sqlPuzzle.select('id', 'name')
sql.from_('table')
sql.columns(('first_name', 'firstName')) # tuple is for AS
sql.from_('table2')
print sql
# output:
# SELECT `id`, `name`, `first_name` AS "firstName" FROM `table`, `table2`

#---- LIMIT --------------------------------------------------------------------

print sqlPuzzle.selectFrom('table').limit(10)
# output: SELECT * FROM `table` LIMIT 10

print sqlPuzzle.selectFrom('table').limit(10).offset(5)
# output: SELECT * FROM `table` LIMIT 10 OFFSET 5

print sqlPuzzle.selectFrom('table').limit(10, 50)
# output: SELECT * FROM `table` LIMIT 10 OFFSET 50

#---- ORDER BY -----------------------------------------------------------------

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

#---- GROUP BY (same as ORDER BY) ----------------------------------------------

sql = sqlPuzzle.selectFrom('table')
sql.groupBy('name')
print sql
# output: SELECT * FROM `table` GROUP BY `name`

sql.groupBy(('name', 'desc'), 'id')
print sql
# output: SELECT * FROM `table` GROUP BY `name` DESC, `id`

sql.groupBy(('name', 'asc')) # or only 'name'
print sql
# output: SELECT * FROM `table` GROUP BY `name`, `id`

