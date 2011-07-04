#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle

print sqlpuzzle.selectFrom('table').limit(10)
# output: SELECT * FROM `table` LIMIT 10

print sqlpuzzle.selectFrom('table').limit(10).offset(5)
# output: SELECT * FROM `table` LIMIT 10 OFFSET 5

print sqlpuzzle.selectFrom('table').limit(10, 50)
# output: SELECT * FROM `table` LIMIT 10 OFFSET 50
