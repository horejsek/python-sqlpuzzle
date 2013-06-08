#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

import sqlpuzzle
import sqlpuzzle.exceptions


sql = sqlpuzzle.update('table')
sql.set(name='Harry')

try:
    print sql
except sqlpuzzle.exceptions.ConfirmUpdateAllException:
    pass  # update all records is not enabled by default

sql.allow_update_all()
print sql
# output: UPDATE `table` SET `name` = "Harry"

try:
    sql.forbid_update_all()
    print sql
except sqlpuzzle.exceptions.ConfirmUpdateAllException:
    pass  # protected of update all records can be turned on again

sql.where(id=42)
print sql
# output: UPDATE `table` SET `name` = "Harry" WHERE `id` = 42

sql.set({
    'age': 21,
    'enabled': True,
})

sql.set('last_modify', datetime.datetime(2011, 6, 15))

values = (
    ('salary', 12000),
    ('enabled', False),
)
sql.set(values)

print sql
#
# output:
# (for better reading splited to more lines)
#
# UPDATE `table` SET
# `salary` = 12000,
# `last_modify` = "2011-06-15T00:00:00",
# `name` = "Harry",
# `age` = 21,
# `enabled` = 0
# WHERE `id` = 42
#
