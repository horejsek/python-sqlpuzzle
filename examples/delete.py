#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlpuzzle
import sqlpuzzle.exceptions


sql = sqlpuzzle.delete().from_('table')

try:
    print sql
except sqlpuzzle.exceptions.ConfirmDeleteAllException:
    pass  # delete all records is not enabled by default

sql.allow_delete_all()
print sql
# output: DELETE FROM `table`

try:
    sql.forbid_delete_all()
    print sql
except sqlpuzzle.exceptions.ConfirmDeleteAllException:
    pass  # protected of delete all records can be turned on again

sql.where(id=42)
print sql
# output: DELETE FROM `table` WHERE `id` = 42

print sqlpuzzle.delete_from('table').where(id=42)
# same output as previous command
