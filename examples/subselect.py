#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle
import sqlpuzzle.relations

subselect = sqlpuzzle.select('name').from_('user').where('id', 42)
print sqlpuzzle.select(subselect).from_('table')
# output:
# SELECT (SELECT `name` FROM `user` WHERE `id` = 42) FROM `table`

subselect = sqlpuzzle.selectFrom('user')
print sqlpuzzle.selectFrom(subselect)
# ouput:
# SELECT * FROM (SELECT * FROM `user`)

subselect = sqlpuzzle.select('id').from_('user').where('name', 'Alan').limit(1)
print sqlpuzzle.selectFrom('table').where(subselect, 50, sqlpuzzle.relations.GE)
# ouput:
# SELECT * FROM `table` WHERE (SELECT `id` FROM `user` WHERE `name` = "Alan" LIMIT 1) >= 50

# if you need column reference in value of condition, just add back quotes (first block is enought)
subselect = sqlpuzzle.select('name').from_(('user', 'parent')).where('parent.id', '`user`.parent_id')
print sqlpuzzle.select('user.*', (subselect, 'parentName')).from_('user')
# output:
# SELECT `user`.*, (SELECT `name` FROM `user` AS `parent` WHERE `parent`.`id` = `user`.`parent_id`) AS "parentName" FROM `user`

