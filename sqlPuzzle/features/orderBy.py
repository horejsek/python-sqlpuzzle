# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.features.order


class OrderBy(sqlPuzzle.features.order.Orders):
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

