import copy

__all__ = ('Object',)


class Object(object):
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, str(self))

    def __str__(self):
        return self.__unicode__() or '<Object>'

    def __unicode__(self):
        return ''

    def tosql(self):
        return self.__str__()

    def copy(self):
        return copy.deepcopy(self)
