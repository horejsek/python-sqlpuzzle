# pylint: disable=redefined-outer-name,invalid-name

import pytest

from sqlpuzzle.exceptions import InvalidArgumentException
from sqlpuzzle._queryparts import Limit


@pytest.fixture
def limit():
    return Limit()


def test_is_not_set(limit):
    assert not limit.is_set


def test_is_set(limit):
    limit.limit(42)
    assert limit.is_set


def test_limit(limit):
    limit.limit(10)
    assert str(limit) == 'LIMIT 10'


def test_offset(limit):
    limit.offset(50)
    assert str(limit) == 'OFFSET 50'


def test_limit_and_offset(limit):
    limit.limit(10)
    limit.offset(50)
    assert str(limit) == 'LIMIT 10 OFFSET 50'


def test_limit_and_offset_in_one(limit):
    limit.limit(5, 15)
    assert str(limit) == 'LIMIT 5 OFFSET 15'


def test_inline(limit):
    limit.limit(3).offset(12)
    assert str(limit) == 'LIMIT 3 OFFSET 12'


def test_inline_invert(limit):
    limit.offset(16).limit(4)
    assert str(limit) == 'LIMIT 4 OFFSET 16'


def test_copy(limit):
    limit.limit(3)
    copy = limit.copy()
    limit.offset(12)
    assert str(copy) == 'LIMIT 3'
    assert str(limit) == 'LIMIT 3 OFFSET 12'


def test_equals(limit):
    limit.limit(3)
    copy = limit.copy()
    assert limit == copy


def test_not_equals(limit):
    limit.limit(3)
    copy = limit.copy()
    limit.offset(12)
    assert not limit == copy


def test_limit_string_exception(limit):
    with pytest.raises(InvalidArgumentException):
        limit.limit('limit')


def test_limit_float_exception(limit):
    with pytest.raises(InvalidArgumentException):
        limit.limit(1.2)


def test_limit_boolean_exception(limit):
    with pytest.raises(InvalidArgumentException):
        limit.limit(False)


def test_offset_string_exception(limit):
    with pytest.raises(InvalidArgumentException):
        limit.offset('offset')


def test_offset_float_exception(limit):
    with pytest.raises(InvalidArgumentException):
        limit.offset(1.2)


def test_offset_boolean_exception(limit):
    with pytest.raises(InvalidArgumentException):
        limit.offset(False)
