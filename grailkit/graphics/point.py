# -*- coding: UTF-8 -*-
"""
    grailkit.graphics.point
    ~~~~~~~~~~~~~~~~~~~~~~~

    Representation of 2d point

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
import math


class Point(object):
    """2d point representation"""

    __slots__ = ['x', 'y']

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __len__(self):
        return self.length()

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        return Point(self.x / other.x, self.y / other.y)

    def __floordiv__(self, other):
        return Point(self.x // other.x, self.y // other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y

    def __imul__(self, other):
        self.x *= other.x
        self.y *= other.y

    def __itruediv__(self, other):
        self.x /= other.x
        self.y /= other.y

    def __ifloordiv__(self, other):
        self.x //= other.x
        self.y //= other.y

    def __eq__(self, other):
        return self.x == other.y and self.y == other.y

    def __ne__(self, other):
        return self.x != other.y and self.y != other.y

    def __lt__(self, other):
        return self.length() < other.length()

    def __le__(self, other):
        return self.length() <= other.length()

    def __gt__(self, other):
        return self.length() > other.length()

    def __ge__(self, other):
        return self.length() >= other.length()

    def __bool__(self):
        return self.x != 0 and self.y != 0

    def length(self):
        """Returns length from (0, 0) to point"""

        return math.sqrt((0 - self.x) ** 2 + (0 - self.y) ** 2)
