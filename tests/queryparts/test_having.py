# pylint: disable=redefined-outer-name,invalid-name

import pytest

import sqlpuzzle
from sqlpuzzle import Q
from sqlpuzzle._queryparts import Having


@pytest.fixture
def having():
    return Having()


def test_is_not_set(having):
    assert not having.is_set


def test_is_set(having):
    having.where(name='Alan')
    assert having.is_set


def test_where_by_tuple(having):
    having.where((
        ('name', 'Harry'),
        ('sex', sqlpuzzle.relations.NE('female')),
        ('age', sqlpuzzle.relations.GT(20)),
    ))
    assert str(having) == 'HAVING "name" = \'Harry\' AND "sex" != \'female\' AND "age" > 20'


def test_where_by_list(having):
    having.where([
        ['name', sqlpuzzle.relations.LIKE('Harry')],
        ['sex', sqlpuzzle.relations.NE('female')],
        ['age', sqlpuzzle.relations.LE(20)],
    ])
    assert str(having) == 'HAVING "name" LIKE \'Harry\' AND "sex" != \'female\' AND "age" <= 20'


def test_where_by_dictionary(having):
    having.where({
        'name': 'Alan',
        'age': 20,
    })
    assert str(having) == 'HAVING "age" = 20 AND "name" = \'Alan\''


def test_where_by_args(having):
    having.where('age', sqlpuzzle.relations.LT(20))
    assert str(having) == 'HAVING "age" < 20'


def test_where_by_kwargs(having):
    having.where(name='Alan')
    assert str(having) == 'HAVING "name" = \'Alan\''


def test_serial_where(having):
    having.where(name='Alan')
    having.where(age=42)
    assert str(having) == 'HAVING "name" = \'Alan\' AND "age" = 42'


def test_str(having):
    having.where(name='ščřž')
    assert str(having) == 'HAVING "name" = \'ščřž\''


def test_more_same_conditions_print_as_one(having):
    having.where(('age', 20), ('age', 20))
    assert str(having) == 'HAVING "age" = 20'


def test_more_same_conditions_with_diff_relation_print_as_more(having):
    having.where(('age', 20), ('age', sqlpuzzle.relations.NE(20)))
    assert str(having) == 'HAVING "age" = 20 AND "age" != 20'


def test_copy(having):
    having.where({'id': 42})
    copy = having.copy()
    having.where({'name': 'Alan'})
    assert str(copy) == 'HAVING "id" = 42'
    assert str(having) == 'HAVING "id" = 42 AND "name" = \'Alan\''


def test_equals(having):
    having.where({'id': 42})
    copy = having.copy()
    assert having == copy


def test_not_equals(having):
    having.where({'id': 42})
    copy = having.copy()
    having.where({'name': 'Alan'})
    assert not having == copy


def test_value_as_integer(having):
    having.where('col', 42)
    assert str(having) == 'HAVING "col" = 42'


def test_value_as_float(having):
    having.where('col', 42.1)
    assert str(having) == 'HAVING "col" = 42.10000'


def test_value_as_boolean(having):
    having.where('col', True)
    assert str(having) == 'HAVING "col" = 1'


def test_value_as_list(having):
    having.where(id=(23, 34, 45))
    assert str(having) == 'HAVING "id" IN (23, 34, 45)'


def test_value_as_list_not_in(having):
    having.where('id', sqlpuzzle.relations.NOT_IN(23, 34, 45))
    assert str(having) == 'HAVING "id" NOT IN (23, 34, 45)'


def test_column_as_integer_exception(having):
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        having.where(42, 'val')


def test_column_as_float_exception(having):
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        having.where(42.1, 'val')


def test_column_as_boolean_exception(having):
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        having.where(True, 'val')


def test_simple_or(having):
    having.where(Q(x='y') | Q(y='x'))
    assert str(having) == 'HAVING ("x" = \'y\' OR "y" = \'x\')'


def test_simple_and(having):
    having.where(Q(x='y') & Q(y='x'))
    assert str(having) == 'HAVING ("x" = \'y\' AND "y" = \'x\')'


def test_more_complicated(having):
    having.where((Q(a=1) & Q(b=2)) | Q(c=3))
    assert str(having) == 'HAVING (("a" = 1 AND "b" = 2) OR "c" = 3)'


def test_more_conditions_in_q(having):
    having.where(Q(a=42, b=24) | Q(x='y'))
    assert str(having) == 'HAVING (("a" = 42 AND "b" = 24) OR "x" = \'y\')'
