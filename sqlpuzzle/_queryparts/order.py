# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six

import sqlpuzzle._libs.argsparser
from sqlpuzzle._common import SqlReference, check_type_decorator
from sqlpuzzle.exceptions import InvalidArgumentException
from .queryparts import QueryPart, QueryParts

__all__ = ('Order', 'Orders')


ASC = 'ASC'
DESC = 'DESC'


class Order(QueryPart):
    def __init__(self, column=None, sort=None):
        super(Order, self).__init__()
        self.column_name = column
        self.sort = sort

    def __unicode__(self):
        if self.sort == ASC:
            return six.text_type(SqlReference(self.column_name))
        else:
            return six.u('%s %s') % (
                SqlReference(self.column_name),
                self.sort,
            )

    def __eq__(self, other):
        return (
            type(self) == type(other) and
            self.column_name == other.column_name and
            self.sort == other.sort
        )

    @property
    def column_name(self):
        return self._column_name

    @column_name.setter
    @check_type_decorator(six.string_types + (int,))
    def column_name(self, column_name):
        self._column_name = column_name

    @property
    def sort(self):
        return self._sort

    @sort.setter
    @check_type_decorator(six.string_types + (int, type(None)))
    def sort(self, sort):
        if sort is None:
            sort = ASC
        sort = sort.upper()
        if sort not in (ASC, DESC):
            raise InvalidArgumentException('Type of order can be only %s or %s.' % (ASC, DESC))
        self._sort = sort


class Orders(QueryParts):
    def order(self, *args, **kwds):
        for column_name, sort in sqlpuzzle._libs.argsparser.parse_args_to_list_of_tuples(
            {
                'max_items': 2,
                'allow_dict': True,
            },
            *args,
            **kwds
        ):
            order = self._find_order_by_column_name(column_name)
            if order is None:
                order = Order(column_name, sort)
                self.append_part(order)
            else:
                order.sort = sort

        return self

    def _find_order_by_column_name(self, column_name):
        for order in self._parts:
            if order.column_name == column_name:
                return order
        return None
