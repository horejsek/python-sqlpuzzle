#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle

sql = sqlpuzzle.selectFrom('table')
sql.leftJoin('table2').on('table.id', 'table2.id')
print sql
# output:
# SELECT * FROM `table` LEFT JOIN `table2` ON (`table`.`id` = `table2`.`id`)

sql = sqlpuzzle.selectFrom('table')
sql.rightJoin('table2').on('table.id', 'table2.id')
print sql
# output:
# SELECT * FROM `table` RIGHT JOIN `table2` ON (`table`.`id` = `table2`.`id`)

sql = sqlpuzzle.selectFrom('table')
sql.join('table2').on('table.id', 'table2.id')
print sql
# output:
# SELECT * FROM `table` JOIN `table2` ON (`table`.`id` = `table2`.`id`)

# grouping of joins - left/right & inner with same condition is inner only
sql = sqlpuzzle.selectFrom('table')
sql.join('table2').on('table.id', 'table2.id')
sql.leftJoin('table2').on('table.id', 'table2.id')
print sql
# output:
# SELECT * FROM `table` JOIN `table2` ON (`table`.`id` = `table2`.`id`)

# left/right & inner with different condition is inner and left/right join
sql = sqlpuzzle.selectFrom('table')
sql.join('table2').on('table.id', 'table2.id')
sql.leftJoin('table2').on('table.id2', 'table2.id2')
print sql
# output:
# SELECT * FROM `table` JOIN `table2` ON (`table`.`id` = `table2`.`id`) LEFT JOIN `table2` ON (`table`.`id2` = `table2`.`id2`)

# more conditions
sql = sqlpuzzle.selectFrom('table')
sql.leftJoin('table2').on('table.id', 'table2.id').on('table.id2', 'table2.id2')
print sql
# output:
# SELECT * FROM `table` LEFT JOIN `table2` ON (`table`.`id` = `table2`.`id` AND `table`.`id2` = `table2`.`id2`)
