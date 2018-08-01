# pylint: disable=invalid-name

import sqlpuzzle.exceptions


def test_has_no_property(select1, select2):
    union = select1 | select2
    assert not union.has('tables')
    assert not union.has('values')
    assert not union.has('where')


def test_union(select1, select2):
    assert str(select1 | select2) == 'SELECT * FROM "t1" UNION SELECT * FROM "t2"'


def test_union_all(select1, select2):
    assert str(select1 & select2) == 'SELECT * FROM "t1" UNION ALL SELECT * FROM "t2"'


def test_combine(select1, select2):
    union = select1 & select2 | select1
    assert str(union) == 'SELECT * FROM "t1" UNION ALL SELECT * FROM "t2" UNION SELECT * FROM "t1"'


def test_subselect_in_column_as_union(select1, select2):
    select = sqlpuzzle.select(select1 & select2).from_('t')
    assert str(select) == 'SELECT (SELECT * FROM "t1" UNION ALL SELECT * FROM "t2") FROM "t"'


def test_subselect_in_table_as_union(select1, select2):
    select = sqlpuzzle.select_from(select1 | select2)
    assert str(select) == 'SELECT * FROM (SELECT * FROM "t1" UNION SELECT * FROM "t2")'


def test_copy(select1, select2):
    union = select1 & select2
    copy = union.copy()
    union |= select1
    assert str(copy) == 'SELECT * FROM "t1" UNION ALL SELECT * FROM "t2"'
    assert str(union) == 'SELECT * FROM "t1" UNION ALL SELECT * FROM "t2" UNION SELECT * FROM "t1"'


def test_equals(select1, select2):
    union = select1 & select2
    copy = union.copy()
    assert str(union) == str(copy)


def test_not_equals(select1, select2):
    union = select1 & select2
    copy = union.copy()
    union |= select1
    assert not union == copy
