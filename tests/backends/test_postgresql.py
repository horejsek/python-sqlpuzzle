# pylint: disable=unused-argument

import sqlpuzzle


def test_reference(postgresql):
    sql = sqlpuzzle.select('id').from_('table')
    assert str(sql) == 'SELECT "id" FROM "table"'

def test_boolean(postgresql):
    sql = sqlpuzzle.select_from('table').where({'flag': True})
    assert str(sql) == 'SELECT * FROM "table" WHERE "flag" = true'
