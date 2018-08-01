import sqlpuzzle


def test_customsql_as_key_in_dict():
    custom = sqlpuzzle.customsql('avg(col)')
    sql = sqlpuzzle.select({
        custom: 'acol',
    }).from_('table')
    assert str(sql) == 'SELECT avg(col) AS "acol" FROM "table"'
