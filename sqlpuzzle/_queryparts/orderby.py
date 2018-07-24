from .order import Orders


class OrderBy(Orders):
    _keyword_of_parts = 'ORDER BY'

    def order_by(self, *args, **kwds):
        self.order(*args, **kwds)
        return self
