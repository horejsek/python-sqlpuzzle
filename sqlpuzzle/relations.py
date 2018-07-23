"""
Use relations in conditions. For example:

.. code-block:: python

    >>> sqlpuzzle.select_from('t').where(name=sqlpuzzle.relations.LIKE('M%'))
    <Select: SELECT * FROM "t" WHERE "name" LIKE 'M%'>
"""

import datetime
import decimal
import types

from sqlpuzzle._common.object import Object
from sqlpuzzle._common.utils import force_text, is_sql_instance

from sqlpuzzle.exceptions import InvalidArgumentException


class _RelationValue(Object):
    _string_representation = 'Abstract Relation'
    _allowed_types = ()

    def __init__(self, value):
        super(_RelationValue, self).__init__()
        self._check_value_type(value)
        self._value = value

    def __str__(self):
        return '"%s %s"' % (
            self._string_representation,
            force_text(self._value),
        )

    def tosql(self):
        return self.__str__()

    def __eq__(self, other):
        """Are relations equivalent?"""
        return (
            self.__class__ == other.__class__ and
            self._value == other._value
        )

    def _check_value_type(self, value):
        # isinstance(True, (int, long)) is True => must be special condition
        if (
                not is_sql_instance(value)
                and (
                    (bool not in self._allowed_types and isinstance(value, bool))
                    or not isinstance(value, self._allowed_types)
                )
        ):
            raise InvalidArgumentException('Relation "%s" is not allowed for data type "%s".' % (
                self._string_representation,
                type(value)
            ))

    @property
    def relation(self):
        return self._string_representation

    @property
    def value(self):
        return self._value

    def _format_condition(self, column, value_transformer=lambda value: value):
        return '%(col)s %(rel)s %(val)s' % {
            'col': column,
            'rel': self.relation,
            'val': value_transformer(self.value),
        }


class EQ(_RelationValue):
    """
    Relation ``=``.

    Default relation in most cases.
    """

    _string_representation = '='
    _allowed_types = (str, int, float, decimal.Decimal, bool, datetime.date)
EQUAL_TO = EQ


class NE(EQ):
    """
    Relation ``!=``.
    """
    _string_representation = '!='
NOT_EQUAL_TO = NE


class GT(_RelationValue):
    """
    Relation ``>``.
    """

    _string_representation = '>'
    _allowed_types = (str, int, float, decimal.Decimal, datetime.date)
GRATHER_THAN = GT


class GE(GT):
    """
    Relation ``>=``.
    """

    _string_representation = '>='
GRATHER_THAN_OR_EQUAL_TO = GE


class LT(GT):
    """
    Relation ``<``.
    """

    _string_representation = '<'
LESS_THAN = LT


class LE(GT):
    """
    Relation ``<=``.
    """

    _string_representation = '<='
LESS_THAN_OR_EQUAL_TO = LE


class LIKE(_RelationValue):
    """
    Relation ``LIKE``.
    """

    _string_representation = 'LIKE'
    _allowed_types = (str,)


class NOT_LIKE(LIKE):
    """
    Relation ``NOT LIKE``.
    """

    _string_representation = 'NOT LIKE'


class REGEXP(_RelationValue):
    """
    Relation ``REGEXP``.
    """

    _string_representation = 'REGEXP'
    _allowed_types = (str,)


class IN(_RelationValue):
    """
    Relation ``IN``.

    If you pass ``None`` in list, it will behave correctly:

    .. code-block:: python

        >>> sqlpuzzle.select_from('t').where(col=sqlpuzzle.relations.IN([1,2,None]))
        <Select: SELECT * FROM "t" WHERE ("col" IN (1, 2) OR "col" IS NULL)>
    """

    _string_representation = 'IN'
    _allowed_types = (list, tuple, range, types.GeneratorType)

    def __init__(self, *args):
        if len(args) > 1:
            value = args
        elif len(args) == 1:
            value = args[0]
        else:
            value = []
        try:
            #  Make list copy of value (if it is possible) because generators
            #+ give value only once.
            value = list(value)
        except TypeError:
            pass
        super(IN, self).__init__(value)

    def _format_condition(self, column, value_transformer=lambda value: value):
        template = '%(col)s %(rel)s %(val)s'

        try:
            value = [v for v in self.value if v is not None]
            if None in self.value:
                if value:
                    template = '(' + template + ' OR %(col)s IS NULL)'
                else:
                    template = '%(col)s IS NULL'
        except TypeError:
            # If its not iterable, it can be subselect or something.
            value = self.value

        return template % {
            'col': column,
            'rel': self.relation,
            'val': value_transformer(value),
        }


class NOT_IN(IN):
    """
    Relation ``NOT IN``.

    If you pass ``None`` in list, it will behave correctly:

    .. code-block:: python

        >>> sqlpuzzle.select_from('t').where(col=sqlpuzzle.relations.NOT_IN([1,2,None]))
        <Select: SELECT * FROM "t" WHERE ("col" NOT IN (1, 2) AND "col" IS NOT NULL)>

    .. versionchanged:: 1.7.0
        There was bug that it generated ``("col" NOT IN (1, 2) OR "col" IS NULL)``
        instead of correct condition.
    """

    _string_representation = 'NOT IN'

    def _format_condition(self, column, value_transformer=lambda value: value):
        template = '%(col)s %(rel)s %(val)s'

        try:
            value = [v for v in self.value if v is not None]
            if None in self.value:
                if value:
                    template = '(' + template + ' AND %(col)s IS NOT NULL)'
                else:
                    template = '%(col)s IS NOT NULL'
        except TypeError:
            # If its not iterable, it can be subselect or something.
            value = self.value

        return template % {
            'col': column,
            'rel': self.relation,
            'val': value_transformer(value),
        }


class IS(_RelationValue):
    """
    Relation ``IS``.
    """

    _string_representation = 'IS'
    _allowed_types = (bool, type(None))


class IS_NOT(IS):
    """
    Relation ``IS NOT``.
    """

    _string_representation = 'IS NOT'
