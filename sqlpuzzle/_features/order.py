# -*- coding: utf-8 -*-

import six

import sqlpuzzle._libs.argsparser
import sqlpuzzle._libs.sqlvalue


ASC = 'ASC'
DESC = 'DESC'
ORDERING_TYPES = (ASC, DESC)


class Order(sqlpuzzle._features.Feature):
    def __init__(self, column=None, sort=None):
        """Initialization of Order."""
        super(Order, self).__init__()
        self._column = column
        self.sort(sort)

    def __str__(self):
        """Print part of query."""
        if self._sort == ASC:
            return str(sqlpuzzle._libs.sqlvalue.SqlReference(self._column))
        else:
            return '%s %s' % (
                sqlpuzzle._libs.sqlvalue.SqlReference(self._column),
                self._sort,
            )

    def __eq__(self, other):
        """Are orders equivalent?"""
        return (
            self._column == other._column and
            self._sort == other._sort
        )

    def sort(self, sort=None):
        """Set type of sort (ASC or DESC)."""
        if sort is None:
            sort = ASC

        sort = sort.upper()
        if sort in ORDERING_TYPES:
            self._sort = sort
        else:
            raise sqlpuzzle.exceptions.InvalidArgumentException(
                'Type of order can be only %s.' % ' or '.join(ORDERING_TYPES))


class Orders(sqlpuzzle._features.Features):
    def _find_order_by_name(self, column_name):
        """Find Order instance by column name."""
        for order in self._features:
            if order._column == column_name:
                return order
        return None

    def order(self, *args, **kwds):
        """Set Order."""
        for column_name, sort in sqlpuzzle._libs.argsparser.parse_args_to_list_of_tuples(
            {
                'max_items': 2,
                'allow_dict': True,
                'allowed_data_types': six.string_types + (int,),
            },
            *args,
            **kwds
        ):
            order = self._find_order_by_name(column_name)
            if order is None:
                order = Order(column_name, sort)
                self.append_feature(order)
            else:
                order.sort(sort)

        return self
