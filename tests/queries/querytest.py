
import unittest

import sqlpuzzle.exceptions
import sqlpuzzle._queries


class QueryTest(unittest.TestCase):
    def test_eq(self):
        self.assertFalse(sqlpuzzle._queries.Query() == 'string')
