#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlpuzzle


print(sqlpuzzle.select().from_('table'))
# output: SELECT * FROM `table`

print(sqlpuzzle.select_from('table'))
# same output as previous command


sql = sqlpuzzle.select('id', 'name')
sql.from_('table')
sql.columns(('first_name', 'firstName'))  # tuple is for AS
sql.from_('table2')
print(sql)
# output:
# SELECT `id`, `name`, `first_name` AS "firstName" FROM `table`, `table2`


# You can also use dictionary for AS in columns and tables.
sql = sqlpuzzle.select({'user_id': 'userId'}).from_({'some_table': 'someTable'})
print(sql)
# output:
# SELECT `user_id` AS "userId" FROM `some_table` AS `someTable`

# Named parameter is also possible.
sql = sqlpuzzle.select(user_id='userId').from_(some_table='someTable')
print(sql)
# Same output as before.
