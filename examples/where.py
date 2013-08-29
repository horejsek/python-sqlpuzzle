#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

import sqlpuzzle


sql = sqlpuzzle.select_from('user')

sql.where(id=42)

sql.where(age=20, name='Michael', enabled=True)

sql.where({
    'last_modify': datetime.datetime(2011, 6, 15, 22, 11, 00),
    'right': 'admin',
})

sql.where('column', sqlpuzzle.relations.LE(10)).where('column', sqlpuzzle.relations.GE(10))

sql.where(
    ('id', sqlpuzzle.relations.NOT_IN(range(10, 20, 2))),
    ('name', 'Alan'),
)

conditions = (
    ('salary', sqlpuzzle.relations.GRATHER_THAN(10000)),
    ('lastname', sqlpuzzle.relations.LIKE('%ar%'))
)
sql.where(conditions)

sql.where(sqlpuzzle.Q(answer=42) | sqlpuzzle.Q(answer=24))

print(sql)

#
# output:
# (for better reading splited to more lines)
#
# SELECT * FROM `user` WHERE
# `id` = 42 AND
# `age` = 20 AND
# `enabled` = 1 AND
# `name` = 'Michael' AND
# `last_modify` = '2011-06-15T22:11:00' AND
# `right` = 'admin' AND
# `column` <= 10 AND
# `column` >= 10 AND
# `id` NOT IN (10, 12, 14, 16, 18) AND
# `name` = 'Alan' AND
# `salary` > 10000 AND
# `lastname` LIKE '%ar%' AND
# (`answer` = 42 OR `answer` = 24)
#
