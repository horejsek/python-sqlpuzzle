import sqlpuzzle
from sqlpuzzle._common import SqlValue, SqlReference
from sqlpuzzle._queryparts import Column


def test_select_test():
    sql = sqlpuzzle.select(1)
    assert str(sql) == 'SELECT 1'


def test_select_without_columns():
    sql = sqlpuzzle.select().from_('user')
    assert str(sql) == 'SELECT * FROM "user"'


def test_select_with_columns():
    sql = sqlpuzzle.select('id', 'name').from_('user')
    assert str(sql) == 'SELECT "id", "name" FROM "user"'


def test_select_from():
    sql = sqlpuzzle.select_from('user')
    assert str(sql) == 'SELECT * FROM "user"'


def test_select_from_as_kwds():
    sql = sqlpuzzle.select_from(user='u')
    assert str(sql) == 'SELECT * FROM "user" AS "u"'


def test_select_from_with_more():
    sql = sqlpuzzle.select_from('user', 'country')
    assert str(sql) == 'SELECT * FROM "user", "country"'


def test_insert():
    sql = sqlpuzzle.insert().into('user').values(name='Harry')
    assert str(sql) == 'INSERT INTO "user" ("name") VALUES (\'Harry\')'


def test_insert_into():
    sql = sqlpuzzle.insert_into('user').values(name='Harry')
    assert str(sql) == 'INSERT INTO "user" ("name") VALUES (\'Harry\')'


def test_update():
    sql = sqlpuzzle.update('user').set(name='Alan').where(id=42)
    assert str(sql) == 'UPDATE "user" SET "name" = \'Alan\' WHERE "id" = 42'


def test_delete():
    sql = sqlpuzzle.delete().from_('user').where(id=42)
    assert str(sql) == 'DELETE FROM "user" WHERE "id" = 42'


def test_delete_from():
    sql = sqlpuzzle.delete_from('user').where(id=42)
    assert str(sql) == 'DELETE FROM "user" WHERE "id" = 42'


def test_copy1():
    query1 = sqlpuzzle.select_from('t').where('c', sqlpuzzle.relations.GT(1))
    query2 = query1.copy()
    assert str(query1) == str(query2)


def test_copy_with_custom():
    query1 = sqlpuzzle.select_from('t').where(sqlpuzzle.customsql('x'))
    query2 = query1.copy()
    assert str(query1) == str(query2)


def test_compare_column_with_custom():
    custom = sqlpuzzle.customsql('custom')
    column = Column('column')
    assert column != custom  # Do not throw exception.


def test_custom_sql():
    # Do not throw exception InvalidArgumentException.
    sqlpuzzle.relations.EQ(sqlpuzzle.customsql('custom'))
    sqlpuzzle.relations.NE(sqlpuzzle.customsql('custom'))
    sqlpuzzle.relations.GT(sqlpuzzle.customsql('custom'))
    sqlpuzzle.relations.GE(sqlpuzzle.customsql('custom'))
    sqlpuzzle.relations.LT(sqlpuzzle.customsql('custom'))
    sqlpuzzle.relations.LE(sqlpuzzle.customsql('custom'))
    sqlpuzzle.relations.LIKE(sqlpuzzle.customsql('custom'))
    sqlpuzzle.relations.REGEXP(sqlpuzzle.customsql('custom'))
    sqlpuzzle.relations.IN(sqlpuzzle.customsql('custom'))
    sqlpuzzle.relations.NOT_IN(sqlpuzzle.customsql('custom'))
    sqlpuzzle.relations.IS(sqlpuzzle.customsql('custom'))
    sqlpuzzle.relations.IS_NOT(sqlpuzzle.customsql('custom'))


def test_sql_value():
    assert isinstance(sqlpuzzle.V('5'), SqlValue)


def test_sql_reference():
    assert isinstance(sqlpuzzle.R('table'), SqlReference)
