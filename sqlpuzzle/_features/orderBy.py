# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle._features.order


class OrderBy(sqlpuzzle._features.order.Orders):
    def __str__(self):
        """Print order (part of query)."""
        orderBy = "ORDER BY %s" % ', '.join(str(order) for order in self._orders)
        return orderBy
    
    def __repr__(self):
        return "<OrderBy: %s>" % self.__str__()
    
    def orderBy(self, *args):
        """Set ORDER BY."""
        self.order(*args)
        return self

