#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle
import sqlPuzzle.relations

import datetime

sql = sqlPuzzle.selectFrom('user')

sql.where(id=42)

sql.where(age=20, name='Michael', enabled=True)

sql.where({
    'last_modify': datetime.datetime(2011, 6, 15, 22, 11, 00),
    'right': 'admin',
})

sql.where('column', 10, sqlPuzzle.relations.LE).where('column', 10, sqlPuzzle.relations.GE)

sql.where(
    ('id', range(10, 20, 2), sqlPuzzle.relations.NOT_IN),
    ('name', 'Alan'),
)

conditions = (
    ('salary', 10000, sqlPuzzle.relations.GRATHER_THAN),
    ('lastname', '%ar%', sqlPuzzle.relations.LIKE)
)
sql.where(conditions)

print sql

#
# output:
# (for better reading splited to more lines)
#
# SELECT * FROM `user` WHERE
# `id` = 42 AND
# `age` = 20 AND 
# `enabled` = 1 AND 
# `name` = "Michael" AND
# `last_modify` = 2011-06-15T22:11:00 AND 
# `right` = "admin" AND 
# `column` <= 10 AND 
# `column` >= 10 AND 
# `id` NOT IN (10, 12, 14, 16, 18) AND 
# `name` = "Alan" AND 
# `salary` > 10000 AND 
# `lastname` LIKE "%ar%"
#
