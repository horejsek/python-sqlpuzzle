#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlpuzzle


###########################################################################
# !!! Use only if you must, because it can be changed without notice. !!! #
###########################################################################


sql = sqlpuzzle.select_from('t').where(name='Alan').limit(5).offset(10).order_by('id̈́')

print sql._limit
# output: LIMIT 5 OFFSET 10

print sql._where
# output: WHERE `name` = "Alan"

print sql._order_by
# output: ORDER BY `id̈́`

# all parts throw all queries:
# * _columns
# * _group_by
# * _having
# * _into_outfile
# * _limit
# * _on_duplicate_key_update
# * _order_by
# * _tables
# * _values
# * _where
# * _select_options

sql = sqlpuzzle.insert_into('t').values(age=20, name='Michael')

print sql._values
# output: `age` = 20, `name` = "Michael"
# oops! output is for update, not insert!
# all this variables is instances:
print "(%s) VALUES (%s)" % (sql._values.columns(), sql._values.values())
# output: (`age`, `name`) VALUES (20, "Michael")
# and now we have ouput for insert :)


# !! This is not to use! But it's possible. !!
print sqlpuzzle._features.limit.Limit().limit(10)
print sqlpuzzle._features.orderby.OrderBy().order_by('id')
# etc..


try:
    # only for read ;)
    sql._tables = sqlpuzzle._features.tables.Tables().set('table')
except AttributeError, e:
    print e
