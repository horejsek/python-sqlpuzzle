# pylint: disable=invalid-name

import sqlpuzzle.exceptions
import sqlpuzzle.relations


def test_simply(update):
    update.table('user')
    update.set(name='Alan')
    update.allow_update_all()
    assert str(update) == 'UPDATE "user" SET "name" = \'Alan\''


def test_str(update):
    update.table('user')
    update.set(name='ščřž')
    update.allow_update_all()
    assert str(update) == 'UPDATE "user" SET "name" = \'ščřž\''


def test_where(update):
    update.table('user')
    update.set(name='Alan')
    update.where(age=42)
    update.where('name', sqlpuzzle.relations.LIKE('Harry'))
    update.where({
        'sex': 'male',
    })
    update.where((
        ('enabled', 1),
    ))
    assert str(update) == (
        'UPDATE "user" SET "name" = \'Alan\''
        ' WHERE "age" = 42 AND "name" LIKE \'Harry\' AND "sex" = \'male\' AND "enabled" = 1'
    )


def test_copy(update):
    update.table('user').set(name='Alan').where(id=42)
    copy = update.copy()
    update.set(age=24)
    assert str(copy) == 'UPDATE "user" SET "name" = \'Alan\' WHERE "id" = 42'
    assert str(update) == 'UPDATE "user" SET "name" = \'Alan\', "age" = 24 WHERE "id" = 42'


def test_equals(update):
    update.table('user').set(name='Alan').where(id=42)
    copy = update.copy()
    assert update == copy


def test_not_equals(update):
    update.table('user').set(name='Alan').where(id=42)
    copy = update.copy()
    update.set(age=24)
    assert not update == copy


def test_join(update):
    update.table('user')
    update.join('test_user')
    update.on('user.id', 'test_user.id')
    update.set(name='Alan')
    update.where(age=42)
    update.allow_update_all()
    assert str(update) == (
        'UPDATE "user" JOIN "test_user" ON "user"."id" = "test_user"."id" SET "name" = \'Alan\' WHERE "age" = 42'
    )


def test_inner_join(update):
    update.table('user')
    update.inner_join('test_user')
    update.on('user.id', 'test_user.id')
    update.set(name='Alan')
    update.where(age=42)
    update.allow_update_all()
    assert str(update) == (
        'UPDATE "user" JOIN "test_user" ON "user"."id" = "test_user"."id" SET "name" = \'Alan\' WHERE "age" = 42'
    )


def test_left_join(update):
    update.table('user')
    update.left_join('test_user')
    update.on('user.id', 'test_user.id')
    update.set(name='Alan')
    update.where(age=42)
    update.allow_update_all()
    assert str(update) == (
        'UPDATE "user" LEFT JOIN "test_user" ON "user"."id" = "test_user"."id" SET "name" = \'Alan\' WHERE "age" = 42'
    )


def test_right_join(update):
    update.table('user')
    update.right_join('test_user')
    update.on('user.id', 'test_user.id')
    update.set(name='Alan')
    update.where(age=42)
    update.allow_update_all()
    assert str(update) == (
        'UPDATE "user" RIGHT JOIN "test_user" ON "user"."id" = "test_user"."id" SET "name" = \'Alan\' WHERE "age" = 42'
    )


def test_sql_cache(update):
    update.table('table').set(col='val').where(id=1).ignore()
    assert str(update) == 'UPDATE IGNORE "table" SET "col" = \'val\' WHERE "id" = 1'
