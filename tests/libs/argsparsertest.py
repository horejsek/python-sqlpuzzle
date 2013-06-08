
import unittest

import sqlpuzzle.exceptions
from sqlpuzzle._libs.argsparser import parse_args_to_list_of_tuples as parser


class ArgsParserTest(unittest.TestCase):
    pass


class DefaultTest(ArgsParserTest):
    def test_args1(self):
        self.assertEqual(parser({}, 1), [(1,)])

    def test_args2(self):
        self.assertEqual(parser({}, 1, 2), [(1,), (2,)])

    def test_list(self):
        self.assertEqual(parser({}, [1,]), [(1,)])

    def test_tuple(self):
        self.assertEqual(parser({}, (1,)), [(1,)])


class ExceptionsTest(ArgsParserTest):
    def test_kwds_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.SqlPuzzleException, parser, {}, arg=1)

    def test_dictionary_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.SqlPuzzleException, parser, {}, {'key': 1})

    def test_too_many_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.SqlPuzzleException, parser, {}, (1, 2))


class OptionMinItemsTest(ArgsParserTest):
    def test_min2_args1_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.SqlPuzzleException, parser, {'min_items': 2, 'max_items': 2}, 1)

    def test_min2_args2(self):
        self.assertEqual(parser({'min_items': 2, 'max_items': 2}, 1, 2), [(1, 2)])

    def test_min2_ist(self):
        self.assertEqual(parser({'min_items': 2, 'max_items': 2}, [1, 2]), [(1, 2)])

    def test_min2_tuple(self):
        self.assertEqual(parser({'min_items': 2, 'max_items': 2}, (1, 2)), [(1, 2)])

    def test_min_bigger_than_max_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.SqlPuzzleException, parser, {'min_items': 2})

    def test_too_few_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, parser, {'min_items': 2, 'max_items': 2}, "arg")


class OptionMaxItemsTest(ArgsParserTest):
    def test_max2_args1(self):
        self.assertEqual(parser({'max_items': 2}, 1), [(1, None)])

    def test_max2_args2(self):
        self.assertEqual(parser({'max_items': 2}, 1, 2), [(1, None), (2, None)])

    def test_max2_args3(self):
        self.assertEqual(parser({'max_items': 2}, 1, 2, 3), [(1, None), (2, None), (3, None)])

    def test_max2_list(self):
        self.assertEqual(parser({'max_items': 2}, [1, 2], 3), [(1, 2), (3, None)])

    def test_max2_tuple(self):
        self.assertEqual(parser({'max_items': 2}, (1, 2), 3), [(1, 2), (3, None)])

    def test_too_many_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, parser, {'min_items': 2, 'max_items': 2}, "arg1", "arg2", "arg3")


class OptionAllowDictionaryTest(ArgsParserTest):
    def test_args(self):
        self.assertEqual(parser({'allow_dict': True, 'max_items': 2}, {'key': 1}), [('key', 1)])

    def test_kwds(self):
        self.assertEqual(parser({'allow_dict': True, 'max_items': 2}, key=1), [('key', 1)])

    def test_too_few_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.SqlPuzzleException, parser, {'allow_dict': True}, "arg")

    def test_dictionary_must_be_only_one_argument_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.SqlPuzzleException, parser, {'allow_dict': True, 'max_items': 2}, {'key': 1}, "some arg")


class OptionAllowListTest(ArgsParserTest):
    def test_args(self):
        self.assertEqual(parser({'allow_list': True}, 1, 2, 3), [(1,), (2,), (3,)])

    def test_list(self):
        self.assertEqual(parser({'allow_list': True}, (1, 2, 3)), [(1,), (2,), (3,)])


class OptionAllowedDataTypesTest(ArgsParserTest):
    def test_simple(self):
        self.assertEqual(parser({'allowed_data_types': (int, long, float)}, 2), [(2,)])

    def test_simple_exceptions(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, parser, {'allowed_data_types': (int, long, float)}, "string")

    def test_set_for_each_argument(self):
        self.assertEqual(parser({'allowed_data_types': ((int, long, float), (str, unicode)), 'max_items': 2}, (2, "string")), [(2, "string")])

    def test_set_for_each_argument_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, parser, {'allowed_data_types': ((int, long, float), (str, unicode)), 'max_items': 2}, ("string", 2))
