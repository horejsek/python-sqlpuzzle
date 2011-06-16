#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle


print sqlPuzzle.select().from_('table')
# output: SELECT * FROM `table`

print sqlPuzzle.selectFrom('table')
# same output as previous command


sql = sqlPuzzle.select('id', 'name')
sql.from_('table')
sql.columns(('first_name', 'firstName')) # tuple is for AS
sql.from_('table2')
print sql
# output:
# SELECT `id`, `name`, `first_name` AS "firstName" FROM `table`, `table2`
