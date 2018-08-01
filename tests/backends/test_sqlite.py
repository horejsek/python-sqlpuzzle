# pylint: disable=unused-argument

import sqlpuzzle


def test_reference(sqlite):
    sql = sqlpuzzle.select('id').from_('table')
    assert str(sql) == 'SELECT "id" FROM "table"'

def test_boolean(sqlite):
    sql = sqlpuzzle.select_from('table').where({'flag': True})
    assert str(sql) == 'SELECT * FROM "table" WHERE "flag" = 1'

def test_on_duplicate_key_update(sqlite):
    sql = sqlpuzzle.insert_into('user')
    sql.values(id=1, name='Alan')
    sql.on_duplicate_key_update()
    assert str(sql) == 'REPLACE INTO "user" ("id", "name") VALUES (1, \'Alan\')'
