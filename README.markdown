# sqlpuzzle [![Build Status](https://travis-ci.org/horejsek/python-sqlpuzzle.png?branch=master)](https://travis-ci.org/horejsek/python-sqlpuzzle)

Python library for ease of writing SQL queries. For now only for database MySQL & PostgreSQL.

## Requirements

- Python 2.7 or later.
- Latest version supporting Python 2.6 is 1.3.0.

## Installation

Installation of Python module `sqlpuzzle` is very simple by PyPI:

    $ sudo pip install sqlpuzzle

Or you can install development version by extracting archive and run:

    $ sudo make install

## Documentation

Note: there is also `camelCase` methods which are only aliases to methods described here. It's only for backward compatiblity with version 0.x. It will be removed soon.

```python
import sqlpuzzle
```

### Configure

Right now sqlpuzzle support only two databases – MySQL and PostgreSQL. By default sqlpuzzle generate syntax in plain SQL, if you want to change it, you have to call configure somewhere on start of your app.

```python
sqlpuzzle.configure('mysql')
# or
sqlpuzzle.configure('postgresql')
```

### Select

Probably base query. Lets look at how simply we can do it with sqlpuzzle.

```python
sql = sqlpuzzle.select_from('table').where(id=42)
# SELECT * FROM "table" WHERE "id" = 42
```

#### Select options

```python
sql = sqlpuzzle.select_from('table')
sql.distinct()
sql.sql_calc_found_rows()
# SELECT SQL_CALC_FOUND_ROWS DISTINCT * FROM "table"
```

You can also use:

 * `sql_cache`
 * `sql_no_cache`
 * `all`
 * `distinct`
 * `distinctrow`
 * `sql_small_result`
 * `sql_big_result`
 * `sql_buffer_result`
 * `sql_calc_found_rows`
 * `straight_join`
 * `high_priority`

All these methods have one param `allow` by which you can turn off that select option. Useful when you want in some condition turn it off.

```python
sql = sqlpuzzle.select_from('table')
sql.distinct()
# SELECT DISTINCT * FROM "table"
sql.distinct(allow=False)
# SELECT * FROM "table"
```

Note that not all of them works for every database. For example `SQL_NO_CACHE` is only for MySQL.

#### Columns to select

For now we fetch always all columns. That's not good idea, better is explicitly say what we want.

```python
sql = sqlpuzzle.select('id', 'name').from_('table')
# SELECT "id", "name" FROM "table"
```

Look closer to method `from_`. There have to be underscore because `from` is keyword.

If you need add some columns, you can do that by method `columns`.

```python
sql.columns('email', 'country')
# SELECT "id", "name", "email", "country" FROM "table"
```

How to make aliases is described in own [section](#aliases).

#### Tables

Sometimes we need to fetch data from more tables. sqlpuzzle supports both cartesian product and joins.

```python
sqlpuzzle.select_from('t1', 't2')
# SELECT * FROM "t1", "t2"

sqlpuzzle.select_from('t1').left_join('t2').on('t1.id', 't2.id')
# SELECT * FROM "t1" LEFT JOIN "t2" ON "t1"."id" = "t2"."id"
```

You can also use `join`, `right_join`, `inner_join` or `straight_join`.

#### Conditions (`WHERE`)

We already saw condition in first `select`. But there is more to show.

```python
sql.where(id=42, type='answer')
# SELECT * FROM "t" WHERE "type" = 'answer' AND "id" = 42

```

As you can see, you can pass more conditions. By default is always used `AND`. How to do something more complex?

```python
sql.where((sqlpuzzle.Q(age=20) | sqlpuzzle.Q(age=30)) & sqlpuzzle.Q(country='cz')
# SELECT * FROM "t" WHERE ("age" = 20 OR "age" = 30) AND "country" = 'cz'
```

Ok. What about relations – `IN`, `LIKE` and others?

```python
sql.where(id=range(1, 4))
# SELECT * FROM "t" WHERE "id" IN (1, 2, 3)

sql.where(age=sqlpuzzle.relations.GE(21))
# SELECT * FROM "t" WHERE "age" > 21
```

As you can see, if you pass list, it automatically use relation `IN` by default. But you can use relation which you want (if it's supported for that type; you can't use for example integer with `IN`).

List of all supported relations:

 * `EQ` (and alias `EQUAL_TO`)
 * `NE` (and alias `NOT_EQUAL_TO`)
 * `GT` (and alias `GRATHER_THAN`)
 * `GE` (and alias `GRATHER_THAN_OR_EQUAL_TO`)
 * `LT` (and alias `LESS_THAN`)
 * `LE` (and alias `LESS_THAN_OR_EQUAL_TO`)
 * `LIKE`
 * `REGEXP`
 * `IN` (default for list-like variables)
 * `NOT_IN`
 * `IS` (default for `None`)
 * `IS_NOT`

#### `GROUP BY`

Grouping is very similar to [ordering](#order-by).

#### `HAVING`

Having is very similar to [conditions](#conditions-where).

```python
sql.having(id=42)
# SELECT * FROM "t" HAVING "id" = 42
```

#### `ORDER BY`

```python
sql.order_by('name', 'age')
# SELECT * FROM "t" GROUP BY "name", "age"
```

Change order is same as making [aliases](#aliases):

```python
sql.order_by('name', ('age', 'desc'))
# SELECT * FROM "t" GROUP BY "name", "age" DESC
```

#### `LIMIT` and `OFFSET`

```python
sqlpuzzle.select_from('t').limit(10)
# SELECT * FROM "t" LIMIT 10

sqlpuzzle.select_from('t').offset(5)
# SELECT * FROM "t" OFFSET 5

sqlpuzzle.select_from('t').limit(10, 5)
# SELECT * FROM "t" LIMIT 10 OFFSET 5
```

#### `INTO OUTFILE`

```python
sql.into_outfile('/tmp/out')
# SELECT * FROM "t" INTO OUTFILE '/tmp/out'
```

And also you can use methods `fields_terminated_by`, `lines_terminated_by` and `optionally_enclosed_by`.

#### `SELECT FOR UPDATE`

```python
sql.for_update()
# SELECT * FROM "t" FOR UPDATE
```

This method also have param `allow` as methods for [select options](#select-options) by which you can deactivate `SELECT FOR UPDATE`.

### Insert

I think that it's now straightforward how base insert will look like.

```python
sqlpuzzle.insert_into('table').values(name='Michael')
# INSERT INTO "table" ("name") VALUES ('Michael')
```

#### Multi insert

Just call more times method `values` with different item.

```python
sql = sqlpuzzle.insert_into('table')
sql.values(name='Tom')
sql.values(name='Jerry')
# INSERT INTO "table" ("name") VALUES ('Tom'), ('Jerry')
```

You doesn't have to be worried about order of columns or that you always have to pass all columns.

```python
sql = sqlpuzzle.insert_into('table')
sql.values(a=1)
sql.values(b='a')
INSERT INTO "table" ("a", "b") VALUES (1, NULL), (NULL, 'a')
```

#### `ON DUPLICATE KEY UPDATE`

```python
sqlpuzzle.insert_into('t').values(a=2).on_duplicate_key_update(b=4)
# INSERT INTO "t" ("a") VALUES (2) ON DUPLICATE KEY UPDATE "b" = 4
```

### Update

```python
sqlpuzzle.update('table').set(name='admin').where(id=1)
# UPDATE "table" SET "name" = 'admin' WHERE "id" = 1
```

#### How to update all rows?

There is protection before updating all rows which you can turn on or off by methods `allow_update_all` or `forbid_update_all`.

```python
sqlpuzzle.update('table').set(name='admin')
# raises ConfirmUpdateAllException

sqlpuzzle.update('table').set(name='admin').allow_update_all()
# UPDATE "table" SET "name" = 'admin'
```

### Delete

```python
sqlpuzzle.delete_from('table').where(id=1)
# UPDATE "table" SET "name" = 'admin' WHERE "id" = 1
```

#### How to delete all rows?

It's same as for [update](#update), just methods and exception have different names.

```python
sqlpuzzle.delete_from('t')
# raises ConfirmDeleteAllException

sqlpuzzle.delete_from('t').allow_delete_all()
# DELETE FROM "t"
```

### Union

When you have two select query, you can use `|` or `&` to make `UNION` or `UNION ALL`.

```python
s1 = sqlpuzzle.select_from('t')
s2 = sqlpuzzle.select_from('u')

s1 | s2
# SELECT * FROM "t" UNION SELECT * FROM "u"

s1 & s2
# SELECT * FROM "t" UNION ALL SELECT * FROM "u"
```

### Functions

Databases have some agregate functions. For example `COUNT`. You could use [customsql](#custom-sql) for it, but there is better way for some common functions.

```python
sqlpuzzle.select(sqlpuzzle.count()).from_('users')
# SELECT COUNT(*) FROM `users`

sqlpuzzle.select(sqlpuzzle.avg('age')).from_('users')
# SELECT AVG(`age`) FROM `users`
```

List of all supported functions:

 * `avg` or `avg_distinct`
 * `count`
 * `max` or `max_distinct`
 * `min` or `min_distinct`
 * `sum` or `sum_distinct`
 * `concat`
 * `group_contact`
 * `convert`

#### `GROUP CONCAT`

This function have little bit more methods which you can use.

```python
sqlpuzzle.group_contact('name').order_by('name').separator(',')
# GROUP_CONCAT(`name` ORDER BY `age` SEPARATOR ',')
```

#### `CONVERT`

Second parameter of this function have to be some database type. There is no validation, because it's easier to allow everything and keep validation for database.

```python
sqlpuzzle.convert('col', 'unsigned')
# CONVERT(`a`, UNSIGNED)
```

### Custom SQL

Sometimes you have really complex part of query which you can't write with sqlpuzzle. That doesn't mean you have to write that whole query by yourself. You can use `customsql` or just `C`.

```python
sqlpuzzle.select_from('t').where(sqlpuzzle.C('a=5'))
# SELECT * FROM "t" WHERE a=5
```

You can pass `customsql` everywhere. But be aware – `customsql` does not provide [escaping](#escaping). Maybe better choice will be [sqlvalue](#sql-reference-and-value).

### SQL reference and value

For example conditions for joins uses by default reference on both sides.

```python
sqlpuzzle.select_from('t').left_join('u').on('t.id', 'u.id')
# SELECT * FROM "t" LEFT JOIN "u" ON "t"."id" = "u"."id"
```

When you need use SQL value instead, use explicitly `sqlvalue` or just `V`.

```python
sqlpuzzle.select_from('t').left_join('u').on('t.id', sqlpuzzle.V('hi'))
# SELECT * FROM "t" LEFT JOIN "u" ON "t"."id" = 'hi'
```

Same for SQL references with `sqlreference` or just `R`.

```python
sqlpuzzle.select_from('t', 'u').where('t.id', 'u.id')
# SELECT * FROM "t", "u" WHERE "t"."id" = 'u.id'

sqlpuzzle.select_from('t', 'u').where('t.id', sqlpuzzle.R('u'))
# SELECT * FROM "t", "u" WHERE "t"."id" = "u"."id"
```


### Aliases

Everywhere, where aliases makes sense, you can use this.

```python
sqlpuzzle.select('id', ('name', 'users name'), ('age', 'how old user is'))
# SELECT "id", "name" AS "users name", "age" AS "how old user is"

sqlpuzzle.select({'name': 'users name'})
# SELECT "name" AS "users name"

sqlpuzzle.select(name='users name')
# SELECT "name" AS "users name"
```

Note: every column / table is put only once. Only if you have always different alias is same column / table putted more than once.

```python
sqlpuzzle.select('a', 'a')
# SELECT "a"
sqlpuzzle.select('a', ('a', 'b'))
# SELECT "a", "a" AS "b"
```

### Other tips

#### Methods always returns `self`

That means you can do this:

```python
sqlpuzzle.select('name').from_('table').where(id=42)
```

Instead of:

```python
sql = sqlpuzzle.select('name')
sql.from_('table')
sql.where(id=42)
```

#### Escaping

You doesn't have to do escaping by yourself, sqlpuzzle already do this.

```python
sqlpuzzle.select_from('db.table').where('table.column', "some 'value'")
# SELECT * FROM "db"."table" WHERE "table"."column" = 'some \'value\''
```

As you can see, also dot is recognized. But you can force it.

```python
sqlpuzzle.select_from('"db.table"')
# SELECT * FROM "db.table"
```

#### Be aware for order

It's easy to use dictionary for aliases or for change of order, but don't forget that dictionary doesn't have always same order.

```python
sql.order_by({'b': 'desc', 'a': 'asc'})
# SELECT * FROM "t" ORDER BY "a", "b" DESC
```

For `ORDER BY` or `GROUP BY` is better to use `list`.

#### Clone query

When you need do some base query for two queries, you can use method `copy` to clone that query.

```python
sql = sqlpuzzle.select_from('t')

s1 = sql.copy()
s1.where(id=42)

s2 = sql.copy()
s2.where(id=24)
```

#### Check what query contains

There could be situation when you need to know if for example `distinct` is used.

```python
sql = sqlpuzzle.select_from('t').distinct()
sql.has('distinct')
# True
```

This method have two param. First is for specifing part of query (for example `'where'`) and second is for searching in that part of query. Searching is not so stupid, it looks for words.

```python
sql = sqlpuzzle.select_from('t')
sql.has('where')
# False
sql = sqlpuzzle.select_from('t').where(name='Michael')
sql.has('where')
# True
sql.has('where', 'name')
# True
sql = sqlpuzzle.select_from('t').where(surname='Michael')
sql.has('where', 'name')
# False
```

In first param you can use:

 * `select_options` (in fact you can type here already some select options as above)
 * `columns`
 * `tables`
 * `where`
 * `group_by`
 * `having`
 * `order_by`
 * `limit`
 * `into_outfile`
 * `select_for_update`
 * `values`
 * `on_duplicate_key_update`


Enjoy!
