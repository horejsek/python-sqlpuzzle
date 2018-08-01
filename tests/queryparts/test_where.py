# pylint: disable=redefined-outer-name,invalid-name

import decimal

import pytest

import sqlpuzzle
from sqlpuzzle import Q
from sqlpuzzle._queryparts import Exists, Not, Where


@pytest.fixture
def where():
    return Where()


def test_is_not_set(where):
    assert not where.is_set


def test_is_set(where):
    where.where(name='Alan')
    assert where.is_set


def test_where_by_tuple(where):
    where.where((
        ('name', 'Harry'),
        ('sex', sqlpuzzle.relations.NOT_EQUAL_TO('female')),
        ('age', sqlpuzzle.relations.GRATHER_THAN(20)),
    ))
    assert str(where) == 'WHERE "name" = \'Harry\' AND "sex" != \'female\' AND "age" > 20'


def test_where_by_list(where):
    where.where([
        ['name', sqlpuzzle.relations.LIKE('Harry')],
        ['sex', sqlpuzzle.relations.NOT_EQUAL_TO('female')],
        ['age', sqlpuzzle.relations.LESS_THAN_OR_EQUAL_TO(20)],
    ])
    assert str(where) == 'WHERE "name" LIKE \'Harry\' AND "sex" != \'female\' AND "age" <= 20'


def test_where_by_dictionary(where):
    where.where({
        'name': sqlpuzzle.relations.LIKE('Alan'),
        'age': 20,
    })
    assert str(where) == 'WHERE "age" = 20 AND "name" LIKE \'Alan\''


def test_where_by_args(where):
    where.where('age', sqlpuzzle.relations.LESS_THAN(20))
    assert str(where) == 'WHERE "age" < 20'


def test_where_by_kwargs(where):
    where.where(name='Alan')
    assert str(where) == 'WHERE "name" = \'Alan\''


def test_serial_where(where):
    where.where(name='Alan')
    where.where(age=42)
    assert str(where) == 'WHERE "name" = \'Alan\' AND "age" = 42'


def test_str(where):
    where.where(name='ščřž')
    assert str(where) == 'WHERE "name" = \'ščřž\''


def test_EQ(where):
    where.where('col', sqlpuzzle.relations.EQ(12))
    assert str(where) == 'WHERE "col" = 12'


def test_NE(where):
    where.where('col', sqlpuzzle.relations.NE(12))
    assert str(where) == 'WHERE "col" != 12'


def test_GT(where):
    where.where('col', sqlpuzzle.relations.GT(12))
    assert str(where) == 'WHERE "col" > 12'


def test_GE(where):
    where.where('col', sqlpuzzle.relations.GE(12))
    assert str(where) == 'WHERE "col" >= 12'


def test_LT(where):
    where.where('col', sqlpuzzle.relations.LT(12))
    assert str(where) == 'WHERE "col" < 12'


def test_LE(where):
    where.where('col', sqlpuzzle.relations.LE(12))
    assert str(where) == 'WHERE "col" <= 12'


def test_LIKE(where):
    where.where('col', sqlpuzzle.relations.LIKE('val'))
    assert str(where) == 'WHERE "col" LIKE \'val\''


def test_NOT_LIKE(where):
    where.where('col', sqlpuzzle.relations.NOT_LIKE('val'))
    assert str(where) == 'WHERE "col" NOT LIKE \'val\''


def test_REGEXP(where):
    where.where('col', sqlpuzzle.relations.REGEXP('val'))
    assert str(where) == 'WHERE "col" REGEXP \'val\''


def test_IN(where):
    where.where('col', sqlpuzzle.relations.IN(range(3)))
    assert str(where) == 'WHERE "col" IN (0, 1, 2)'


def test_IN_WITH_NONE(where):
    where.where('col', sqlpuzzle.relations.IN([0, 1, 2, None]))
    assert str(where) == 'WHERE ("col" IN (0, 1, 2) OR "col" IS NULL)'


def test_IN_WITH_NONE_ONLY(where):
    where.where('col', sqlpuzzle.relations.IN([None]))
    assert str(where) == 'WHERE "col" IS NULL'


def test_NOT_IN(where):
    where.where('col', sqlpuzzle.relations.NOT_IN(range(3)))
    assert str(where) == 'WHERE "col" NOT IN (0, 1, 2)'


def test_NOT_IN_WITH_NONE(where):
    where.where('col', sqlpuzzle.relations.NOT_IN([0, 1, 2, None]))
    assert str(where) == 'WHERE ("col" NOT IN (0, 1, 2) AND "col" IS NOT NULL)'


def test_NOT_IN_WITH_NONE_ONLY(where):
    where.where('col', sqlpuzzle.relations.NOT_IN([None]))
    assert str(where) == 'WHERE "col" IS NOT NULL'


def test_IS(where):
    where.where('col', sqlpuzzle.relations.IS(None))
    assert str(where) == 'WHERE "col" IS NULL'


def test_IS_NOT(where):
    where.where('col', sqlpuzzle.relations.IS_NOT(None))
    assert str(where) == 'WHERE "col" IS NOT NULL'


def test_default_relation_of_sql_value_with_number(where):
    where.where('col', sqlpuzzle.V(123))
    assert str(where) == 'WHERE "col" = 123'


def test_default_relation_of_sql_value_with_none(where):
    where.where('col', sqlpuzzle.V(None))
    assert str(where) == 'WHERE "col" IS NULL'


def test_custom_simple(where):
    customsql = sqlpuzzle.customsql('"custom" = "sql" OR "sql" = "custom"')
    where.where(customsql)
    assert str(where) == 'WHERE "custom" = "sql" OR "sql" = "custom"'


def test_more_same_conditions_print_as_one(where):
    where.where(('age', 20), ('age', 20))
    assert str(where) == 'WHERE "age" = 20'


def test_more_same_conditions_with_diff_relation_print_as_more(where):
    where.where(('age', 20), ('age', sqlpuzzle.relations.NE(20)))
    assert str(where) == 'WHERE "age" = 20 AND "age" != 20'


def test_value_as_integer(where):
    where.where('col', 42)
    assert str(where) == 'WHERE "col" = 42'


def test_value_as_float(where):
    where.where('col', 42.1)
    assert str(where) == 'WHERE "col" = 42.10000'


def test_value_as_decimal(where):
    where.where('col', decimal.Decimal('42.1'))
    assert str(where) == 'WHERE "col" = 42.10000'


def test_value_as_boolean(where):
    where.where('col', True)
    assert str(where) == 'WHERE "col" = 1'


def test_value_as_list(where):
    where.where(id=(23, 34, 45))
    assert str(where) == 'WHERE "id" IN (23, 34, 45)'


def test_value_as_list_not_in(where):
    where.where('id', sqlpuzzle.relations.NOT_IN(23, 34, 45))
    assert str(where) == 'WHERE "id" NOT IN (23, 34, 45)'


def test_value_as_generator(where):
    where.where('col', (x for x in range(5)))
    assert str(where) == 'WHERE "col" IN (0, 1, 2, 3, 4)'
    # Second printed version must be same. Generator give values only once!
    assert str(where) == 'WHERE "col" IN (0, 1, 2, 3, 4)'


def test_value_as_xrange(where):
    where.where('id', range(3))
    assert str(where) == 'WHERE "id" IN (0, 1, 2)'


def test_value_as_none(where):
    where.where('col', None)
    assert str(where) == 'WHERE "col" IS NULL'


def test_value_as_not_none(where):
    where.where('col', sqlpuzzle.relations.IS_NOT(None))
    assert str(where) == 'WHERE "col" IS NOT NULL'


def test_copy(where):
    where.where({'id': 42})
    copy = where.copy()
    where.where({'name': 'Alan'})
    assert str(copy) == 'WHERE "id" = 42'
    assert str(where) == 'WHERE "id" = 42 AND "name" = \'Alan\''


def test_equals(where):
    where.where({'id': 42})
    copy = where.copy()
    assert where == copy


def test_not_equals(where):
    where.where({'id': 42})
    copy = where.copy()
    where.where({'name': 'Alan'})
    assert not where == copy


def test_column_as_integer_exception(where):
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        where.where(42, 'val')


def test_column_as_float_exception(where):
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        where.where(42.1, 'val')


def test_column_as_boolean_exception(where):
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        where.where(True, 'val')


def test_value_as_list_wrong_relation_exception():
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        sqlpuzzle.relations.LE((23, 34, 45))
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        sqlpuzzle.relations.NE((23, 34, 45))
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        sqlpuzzle.relations.LIKE((23, 34, 45))


def test_value_as_boolean_wrong_relation_exception():
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        sqlpuzzle.relations.GT(True)
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        sqlpuzzle.relations.NOT_IN(True)
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        sqlpuzzle.relations.LIKE(True)


def test_value_as_integer_wrong_relation_exception():
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        sqlpuzzle.relations.LIKE(67)
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        sqlpuzzle.relations.IN(67)


def test_value_as_string_wrong_relation_exception():
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        sqlpuzzle.relations.NOT_IN(67)
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        sqlpuzzle.relations.IN(67)


def test_simple_or(where):
    where.where(Q(x='y') | Q(y='x'))
    assert str(where) == 'WHERE ("x" = \'y\' OR "y" = \'x\')'


def test_simple_and(where):
    where.where(Q(x='y') & Q(y='x'))
    assert str(where) == 'WHERE ("x" = \'y\' AND "y" = \'x\')'


def test_more_complicated(where):
    where.where((Q(a=1) & Q(b=2)) | Q(c=3))
    assert str(where) == 'WHERE (("a" = 1 AND "b" = 2) OR "c" = 3)'


def test_more_conditions_in_q(where):
    where.where(Q(a=42, b=24) | Q(x='y'))
    assert str(where) == 'WHERE (("a" = 42 AND "b" = 24) OR "x" = \'y\')'


def test_two_qobjects(where):
    where.where(Q(a=1) | Q(a=2), Q(b=1) | Q(b=2))
    assert str(where) == 'WHERE ("a" = 1 OR "a" = 2) AND ("b" = 1 OR "b" = 2)'


def test_three_qobjects(where):
    where.where(Q(a=1) | Q(a=2), Q(b=1) | Q(b=2), Q(c=1))
    assert str(where) == 'WHERE ("a" = 1 OR "a" = 2) AND ("b" = 1 OR "b" = 2) AND "c" = 1'


def test_qobject_in_qobject(where):
    where.where(Q(Q(a=1) | Q(b=2)) & Q(c=3))
    assert str(where) == 'WHERE (("a" = 1 OR "b" = 2) AND "c" = 3)'


def test_not(where):
    where.where(Not(a=1))
    assert str(where) == 'WHERE NOT("a" = 1)'


def test_not_with_q(where):
    where.where(Not(Q(a=1) | Q(b=2)))
    assert str(where) == 'WHERE NOT(("a" = 1 OR "b" = 2))'


def test_exists(where):
    subquery = sqlpuzzle.select_from('t2').where(col=sqlpuzzle.R('t1.col'))
    where.where(Exists(subquery))
    assert str(where) == 'WHERE EXISTS(SELECT * FROM "t2" WHERE "col" = "t1"."col")'
