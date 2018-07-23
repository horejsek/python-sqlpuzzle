
import unittest

from sqlpuzzle._queries import Query


class QueryTest(unittest.TestCase):
    def test_eq(self):
        self.assertFalse(Query() == 'string')

    def test_non_exist_property(self):
        self.assertFalse(Query().has('xxx'))
