#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle

print sqlPuzzle.selectFrom('table').limit(10)
# output: SELECT * FROM `table` LIMIT 10

print sqlPuzzle.selectFrom('table').limit(10).offset(5)
# output: SELECT * FROM `table` LIMIT 10 OFFSET 5

print sqlPuzzle.selectFrom('table').limit(10, 50)
# output: SELECT * FROM `table` LIMIT 10 OFFSET 50
