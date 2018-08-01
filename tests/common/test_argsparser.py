# pylint: disable=invalid-name

import pytest

import sqlpuzzle
from sqlpuzzle._common import parse_args as parser


def test_empty_args1():
    assert parser({}, 1) == [(1,)]


def test_empty_args2():
    assert parser({}, 1, 2) == [(1,), (2,)]


def test_empty_list():
    assert parser({}, [1]) == [(1,)]


def test_empty_tuple():
    assert parser({}, (1,)) == [(1,)]


def test_empty_kwds_exception():
    with pytest.raises(sqlpuzzle.exceptions.SqlPuzzleException):
        parser({}, arg=1)


def test_empty_dictionary_exception():
    with pytest.raises(sqlpuzzle.exceptions.SqlPuzzleException):
        parser({}, {'key': 1})


def test_empty_too_many_exception():
    with pytest.raises(sqlpuzzle.exceptions.SqlPuzzleException):
        parser({}, (1, 2))


def test_min2_args2():
    assert parser({'min_items': 2, 'max_items': 2}, 1, 2) == [(1, 2)]


def test_min2_list():
    assert parser({'min_items': 2, 'max_items': 2}, [1, 2]) == [(1, 2)]


def test_min2_tuple():
    assert parser({'min_items': 2, 'max_items': 2}, (1, 2)) == [(1, 2)]


def test_max2_args1():
    assert parser({'max_items': 2}, 1) == [(1, None)]


def test_max2_args2():
    assert parser({'max_items': 2}, 1, 2) == [(1, None), (2, None)]


def test_max2_args3():
    assert parser({'max_items': 2}, 1, 2, 3) == [(1, None), (2, None), (3, None)]


def test_max2_list():
    assert parser({'max_items': 2}, [1, 2], 3) == [(1, 2), (3, None)]


def test_max2_tuple():
    assert parser({'max_items': 2}, (1, 2), 3) == [(1, 2), (3, None)]


def test_min_bigger_than_max_exception():
    with pytest.raises(AssertionError):
        parser({'min_items': 2, 'max_items': 1})


def test_too_few_exception():
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        parser({'min_items': 2, 'max_items': 2}, 'arg')


def test_too_many_exception():
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        parser({'min_items': 2, 'max_items': 2}, 'arg1', 'arg2', 'arg3')


def test_dict_args():
    assert parser({'allow_dict': True, 'max_items': 2}, {'key': 1}) == [('key', 1)]


def test_dict_kwds():
    assert parser({'allow_dict': True, 'max_items': 2}, key=1) == [('key', 1)]


def test_dict_too_few_exception():
    with pytest.raises(AssertionError):
        parser({'allow_dict': True}, 'arg')


def test_list_args():
    assert parser({'allow_list': True}, 1, 2, 3) == [(1,), (2,), (3,)]


def test_list_list():
    assert parser({'allow_list': True}, (1, 2, 3)) == [(1,), (2,), (3,)]


def test_args_and_kwds():
    assert parser({'allow_dict': True, 'max_items': 2}, 'a', b=2) == [('a', None), ('b', 2)]
