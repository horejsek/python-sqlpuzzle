#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle
import sqlpuzzle.exceptions

sql = sqlpuzzle.delete().from_('table')

try:
    print sql
except sqlpuzzle.exceptions.ConfirmDeleteAllException:
    pass # delete all records is not enabled by default

sql.allowDeleteAll()
print sql
# output: DELETE FROM `table`

try:
    sql.forbidDeleteAll()
    print sql
except sqlpuzzle.exceptions.ConfirmDeleteAllException:
    pass # protected of delete all records can be turned on again

sql.where(id=42)
print sql
# output: DELETE FROM `table` WHERE `id` = 42

print sqlpuzzle.deleteFrom('table').where(id=42)
# same output as previous command
