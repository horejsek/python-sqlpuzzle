
import unittest

import sqlpuzzle.exceptions
from sqlpuzzle._queries import Query


class QueryTest(unittest.TestCase):
    def test_eq(self):
        self.assertFalse(Query() == 'string')
