# -*- coding: utf-8 -*-

import unittest

from sqlpuzzle.exceptions import InvalidArgumentException
from sqlpuzzle._queryparts import Limit


class LimitTest(unittest.TestCase):
    def setUp(self):
        self.limit = Limit()


class BaseTest(LimitTest):
    def test_is_not_set(self):
        self.assertEqual(self.limit.is_set(), False)

    def test_is_set(self):
        self.limit.limit(42)
        self.assertEqual(self.limit.is_set(), True)

    def test_limit(self):
        self.limit.limit(10)
        self.assertEqual(str(self.limit), 'LIMIT 10')

    def test_offset(self):
        self.limit.offset(50)
        self.assertEqual(str(self.limit), 'OFFSET 50')

    def test_limit_and_offset(self):
        self.limit.limit(10)
        self.limit.offset(50)
        self.assertEqual(str(self.limit), 'LIMIT 10 OFFSET 50')

    def test_limit_and_offset_in_one(self):
        self.limit.limit(5, 15)
        self.assertEqual(str(self.limit), 'LIMIT 5 OFFSET 15')


class InlineTest(LimitTest):
    def test_inline(self):
        self.limit.limit(3).offset(12)
        self.assertEqual(str(self.limit), 'LIMIT 3 OFFSET 12')

    def test_inline_invert(self):
        self.limit.offset(16).limit(4)
        self.assertEqual(str(self.limit), 'LIMIT 4 OFFSET 16')


class CopyTest(LimitTest):
    def test_copy(self):
        self.limit.limit(3)
        copy = self.limit.copy()
        self.limit.offset(12)
        self.assertEqual(str(copy), 'LIMIT 3')
        self.assertEqual(str(self.limit), 'LIMIT 3 OFFSET 12')

    def test_equals(self):
        self.limit.limit(3)
        copy = self.limit.copy()
        self.assertTrue(self.limit == copy)

    def test_not_equals(self):
        self.limit.limit(3)
        copy = self.limit.copy()
        self.limit.offset(12)
        self.assertFalse(self.limit == copy)


class ExceptionsTest(LimitTest):
    def test_limit_string_exception(self):
        self.assertRaises(InvalidArgumentException, self.limit.limit, 'limit')

    def test_limit_float_exception(self):
        self.assertRaises(InvalidArgumentException, self.limit.limit, 1.2)

    def test_limit_boolean_exception(self):
        self.assertRaises(InvalidArgumentException, self.limit.limit, False)

    def test_offset_string_exception(self):
        self.assertRaises(InvalidArgumentException, self.limit.offset, 'offset')

    def test_offset_float_exception(self):
        self.assertRaises(InvalidArgumentException, self.limit.offset, 1.2)

    def test_offset_boolean_exception(self):
        self.assertRaises(InvalidArgumentException, self.limit.offset, False)
