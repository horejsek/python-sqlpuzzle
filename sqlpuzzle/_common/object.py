import copy

__all__ = ('Object',)


class Object:
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, str(self))

    def __str__(self):
        return '<Object>'

    def tosql(self):
        return self.__str__()

    def copy(self):
        return copy.deepcopy(self)
