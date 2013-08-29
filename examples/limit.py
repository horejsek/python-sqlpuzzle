#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlpuzzle


print(sqlpuzzle.select_from('table').limit(10))
# output: SELECT * FROM `table` LIMIT 10

print(sqlpuzzle.select_from('table').limit(10).offset(5))
# output: SELECT * FROM `table` LIMIT 10 OFFSET 5

print(sqlpuzzle.select_from('table').limit(10, 50))
# output: SELECT * FROM `table` LIMIT 10 OFFSET 50
