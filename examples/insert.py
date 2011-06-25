#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle
import sqlPuzzle.exceptions

import datetime

sql = sqlPuzzle.insert().into('table')

sql.values(name='Alan')

sql.values({
    'enabled': True,
})

sql.values('age', 42)

sql.values(('salary', 12345.67), ('last_modify', datetime.datetime(2011, 6, 15)))

values = (
    ('age', 21),
    ('loginname', 'alan')
)
sql.values(values)

print sql
#
# output:
# (for better reading splited to more lines)
#
# INSERT INTO `table`
# (`salary`, `last_modify`, `loginname`, `name`, `age`, `enabled`)
# VALUES
# (12345.67000, "2011-06-15T00:00:00", "alan", "Alan", 21, 1)
#

print sqlPuzzle.insertInto('table').values(values)
# output:
# INSERT INTO `table` (`age`, `loginname`) VALUES (21, "alan")
