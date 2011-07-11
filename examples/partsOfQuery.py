#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle

###########################################################################
# !!! Use only if you must, because it can be changed without notice. !!! #
###########################################################################

sql = sqlpuzzle.selectFrom('t').where(name='Alan').limit(5).offset(10).orderBy('id̈́')

print sql._limit
# output: LIMIT 5 OFFSET 10

print sql._where
# output: WHERE `name` = "Alan"

print sql._orderBy
# output: ORDER BY `id̈́`

# all parts throw all queries:
# * _columns
# * _groupBy
# * _having
# * _intoOutfile
# * _limit
# * _onDuplicateKeyUpdate
# * _orderBy
# * _tables
# * _values
# * _where
# * _selectOptions

sql = sqlpuzzle.insertInto('t').values(age=20)

print sql._values
# output: `age` = 20, `name` = "Michael"
# oops! output is for update, not insert!
# all this variables is instances:
print "(%s) VALUES (%s)" % (sql._values.columns(), sql._values.values())
# output: (`age`, `name`) VALUES (20, "Michael")
# and now we have ouput for insert :)


# !! This is not to use! But it's possible. !!
print sqlpuzzle._features.limit.Limit().limit(10)
print sqlpuzzle._features.orderBy.OrderBy().orderBy('id')
# etc..


try:
    # only for read ;)
    sql._tables = sqlpuzzle._features.tables.Tables().set('table')
except:
    pass


