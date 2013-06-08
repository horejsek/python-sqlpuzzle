# -*- coding: utf-8 -*-

import sqlpuzzle._features.order


class OrderBy(sqlpuzzle._features.order.Orders):
    def __init__(self):
        """Initialization of OrderBy."""
        super(OrderBy, self).__init__()
        self._keyword_of_feature = 'ORDER BY'

    def order_by(self, *args, **kwds):
        """Set ORDER BY."""
        self.order(*args, **kwds)
        return self
