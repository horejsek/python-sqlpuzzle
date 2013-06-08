#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlpuzzle


sql = sqlpuzzle.select_from('table')
sql.left_join('table2').on('table.id', 'table2.id')
print sql
# output:
# SELECT * FROM `table` LEFT JOIN `table2` ON (`table`.`id` = `table2`.`id`)

sql = sqlpuzzle.select_from('table')
sql.right_join('table2').on('table.id', 'table2.id')
print sql
# output:
# SELECT * FROM `table` RIGHT JOIN `table2` ON (`table`.`id` = `table2`.`id`)

sql = sqlpuzzle.select_from('table')
sql.join('table2').on('table.id', 'table2.id')
print sql
# output:
# SELECT * FROM `table` JOIN `table2` ON (`table`.`id` = `table2`.`id`)

# grouping of joins - left/right & inner with same condition is inner only
sql = sqlpuzzle.select_from('table')
sql.join('table2').on('table.id', 'table2.id')
sql.left_join('table2').on('table.id', 'table2.id')
print sql
# output:
# SELECT * FROM `table` JOIN `table2` ON (`table`.`id` = `table2`.`id`)

# left/right & inner with different condition is inner and left/right join
sql = sqlpuzzle.select_from('table')
sql.join('table2').on('table.id', 'table2.id')
sql.left_join('table2').on('table.id2', 'table2.id2')
print sql
# output:
# SELECT * FROM `table` JOIN `table2` ON (`table`.`id` = `table2`.`id`) LEFT JOIN `table2` ON (`table`.`id2` = `table2`.`id2`)

# more conditions
sql = sqlpuzzle.select_from('table')
sql.left_join('table2').on('table.id', 'table2.id').on('table.id2', 'table2.id2')
print sql
# output:
# SELECT * FROM `table` LEFT JOIN `table2` ON (`table`.`id` = `table2`.`id` AND `table`.`id2` = `table2`.`id2`)
