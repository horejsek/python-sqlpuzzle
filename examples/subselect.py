#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle
import sqlPuzzle.relations

subselect = sqlPuzzle.select('name').from_('user').where('id', 42)
print sqlPuzzle.select(subselect).from_('table')
# output:
# SELECT (SELECT `name` FROM `user` WHERE `id` = 42) FROM `table`

subselect = sqlPuzzle.selectFrom('user')
print sqlPuzzle.selectFrom(subselect)
# ouput:
# SELECT * FROM (SELECT * FROM `user`)

subselect = sqlPuzzle.select('id').from_('user').where('name', 'Alan').limit(1)
print sqlPuzzle.selectFrom('table').where(subselect, 50, sqlPuzzle.relations.GE)
# ouput:
# SELECT * FROM `table` WHERE (SELECT `id` FROM `user` WHERE `name` = "Alan" LIMIT 1) >= 50

# if you need column reference in value of condition, just add back quotes (first block is enought)
subselect = sqlPuzzle.select('name').from_(('user', 'parent')).where('parent.id', '`user`.parent_id')
print sqlPuzzle.select('user.*', (subselect, 'parentName')).from_('user')
# output:
# SELECT `user`.*, (SELECT `name` FROM `user` AS `parent` WHERE `parent`.`id` = `user`.`parent_id`) AS "parentName" FROM `user`

