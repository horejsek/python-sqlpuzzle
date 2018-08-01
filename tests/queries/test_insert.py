# pylint: disable=invalid-name,unused-argument


def test_simply(insert):
    insert.into('user')
    insert.values(name='Alan')
    assert str(insert) == 'INSERT INTO "user" ("name") VALUES (\'Alan\')'


def test_str(insert):
    insert.into('user')
    insert.values(name='ščřž')
    assert str(insert) == 'INSERT INTO "user" ("name") VALUES (\'ščřž\')'


def test_has_not_tables(insert):
    assert not insert.has('tables')


def test_has_tables(insert):
    insert.into('user')
    assert insert.has('tables')
    assert insert.has('tables', 'user')


def test_has_not_values(insert):
    assert not insert.has('values')


def test_has_values(insert):
    insert.values(id=1)
    assert insert.has('values')
    assert insert.has('values', '1')


def test_on_duplicate_key_update(insert, postgresql):
    insert.into('user')
    values = {
        'name': 'Alan',
    }
    insert.values(id=1, **values)
    insert.on_duplicate_key_update('id', values)
    assert str(insert) == (
        'INSERT INTO "user" ("id", "name") VALUES (1, \'Alan\') ON CONFLICT ("id") DO UPDATE "name" = \'Alan\''
    )


def test_on_conflict_do_update(insert, mysql):
    insert.into('user')
    values = {
        'name': 'Alan',
    }
    insert.values(id=1, **values)
    insert.on_duplicate_key_update(values)
    assert str(insert) == (
        'INSERT INTO `user` (`id`, `name`) VALUES (1, \'Alan\') ON DUPLICATE KEY UPDATE `name` = \'Alan\''
    )


def test_copy(insert):
    insert.into('user').values(id=1)
    copy = insert.copy()
    insert.values(id=2)
    assert str(copy) == 'INSERT INTO "user" ("id") VALUES (1)'
    assert str(insert) == 'INSERT INTO "user" ("id") VALUES (1), (2)'


def test_equals(insert):
    insert.into('user').values(id=1)
    copy = insert.copy()
    assert insert == copy


def test_not_equals(insert):
    insert.into('user').values(id=1)
    copy = insert.copy()
    insert.values(name='Alan')
    assert not insert == copy


def test_multiple_inserts(insert):
    insert.into('table').values(id=1).values(id=2).values(id=3)
    assert str(insert) == 'INSERT INTO "table" ("id") VALUES (1), (2), (3)'


def test_sql_cache(insert):
    insert.into('table').values(id=1).ignore()
    assert str(insert) == 'INSERT IGNORE INTO "table" ("id") VALUES (1)'
