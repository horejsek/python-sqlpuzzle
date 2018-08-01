# pylint: disable=invalid-name

import sqlpuzzle.exceptions


def test_simply(delete):
    delete.from_('user')
    delete.allow_delete_all()
    assert str(delete) == 'DELETE FROM "user"'


def test_str(delete):
    delete.from_('user')
    delete.where(name='ščřž')
    assert str(delete) == 'DELETE FROM "user" WHERE "name" = \'ščřž\''


def test_has_not_references(delete):
    assert not delete.has('references')


def test_has_references(delete):
    delete.from_('user')
    assert delete.has('references')
    assert delete.has('references', 'user')


def test_has_not_where(delete):
    assert not delete.has('where')


def test_has_where(delete):
    delete.where(id=1)
    assert delete.has('where')
    assert delete.has('where', 'id')


def test_more_tables(delete):
    delete.allow_delete_all()
    delete.delete('user').from_('user', 'user2')
    assert str(delete) == 'DELETE "user" FROM "user", "user2"'


def test_more_tables_with_alias(delete):
    delete.allow_delete_all()
    delete.delete('u').from_({'user': 'u', 'user2': 'u2'})
    assert str(delete) == 'DELETE "u" FROM "user" AS "u", "user2" AS "u2"'


def test_join(delete):
    delete.allow_delete_all()
    delete.delete('user').from_('user').left_join('role').on('role.id', 'user.role_id').where('role.name', ('a', 'b'))
    assert str(delete) == (
        'DELETE "user" FROM "user" LEFT JOIN "role" ON "role"."id" = "user"."role_id"'
        ' WHERE "role"."name" IN (\'a\', \'b\')'
    )


def test_where(delete):
    delete.from_('user')
    delete.where(age=42)
    delete.where('name', sqlpuzzle.relations.LIKE('Harry'))
    delete.where({
        'sex': 'male',
    })
    delete.where((
        ('enabled', 1),
    ))
    assert str(delete) == (
        'DELETE FROM "user" WHERE "age" = 42 AND "name" LIKE \'Harry\' AND "sex" = \'male\' AND "enabled" = 1'
    )


def test_copy(delete):
    delete.from_('user').where(id=42)
    copy = delete.copy()
    delete.where(name='Harry')
    assert str(copy) == 'DELETE FROM "user" WHERE "id" = 42'
    assert str(delete) == 'DELETE FROM "user" WHERE "id" = 42 AND "name" = \'Harry\''


def test_equals(delete):
    delete.from_('user').where(id=42)
    copy = delete.copy()
    assert delete == copy


def test_not_equals(delete):
    delete.from_('user').where(id=42)
    copy = delete.copy()
    delete.where(name='Harry')
    assert not delete == copy


def test_sql_cache(delete):
    delete.from_('table').where(id=1).ignore()
    assert str(delete) == 'DELETE IGNORE FROM "table" WHERE "id" = 1'
