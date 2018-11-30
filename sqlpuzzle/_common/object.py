import copy
from functools import total_ordering

__all__ = ('Object',)


@total_ordering
class Object:
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, str(self))

    def __str__(self):
        return '<Object>'

    def __eq__(self, other):
        """
        Compare functionality supporting comparing with simple string.
        Because Python 3 sort dicts random, we need to sort all items
        to produce the same query (to not miss the cache or to have
        simpler debugging), but in the query can be mix of strings and
        our objects (like custom, sqlvalue and so on).
        """
        if isinstance(other, str):
            return str(self) == other
        elif isinstance(other, Object):
            return str(self) == str(other)
        return super().__eq__(other)

    def __lt__(self, other):
        if isinstance(other, str):
            return str(self) < other
        elif isinstance(other, Object):
            return str(self) < str(other)
        return super().__lt__(other)

    def __hash__(self):
        """
        When compare functionality is defined, hash have to be defined
        manually to keep the object hashable. This is the default
        implementation.
        """
        return id(self)

    def tosql(self):
        return self.__str__()

    def copy(self):
        return copy.deepcopy(self)
