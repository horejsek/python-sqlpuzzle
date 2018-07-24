from .order import Orders

__all__ = ('GroupBy',)


class GroupBy(Orders):
    _keyword_of_parts = 'GROUP BY'

    def group_by(self, *args, **kwds):
        self.order(*args, **kwds)
        return self
