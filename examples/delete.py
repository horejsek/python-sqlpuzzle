#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle
import sqlPuzzle.exceptions

sql = sqlPuzzle.delete().from_('table')

try:
    print sql
except sqlPuzzle.exceptions.ConfirmDeleteAllException:
    pass # delete all records is not enabled by default

sql.allowDeleteAll()
print sql
# output: DELETE FROM `table`

try:
    sql.forbidDeleteAll()
    print sql
except sqlPuzzle.exceptions.ConfirmDeleteAllException:
    pass # protected of delete all records can be turned on again

sql.where(id=42)
print sql
# output: DELETE FROM `table` WHERE `id` = 42

print sqlPuzzle.deleteFrom('table').where(id=42)
# same output as previous command
