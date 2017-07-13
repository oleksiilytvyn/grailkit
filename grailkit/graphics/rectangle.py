# -*- coding: UTF-8 -*-
"""
    grailkit.graphics.rectangle
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Representation of 2d rectangle

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
from .point import Point


class Rectangle(object):
    """2d rectangle in 2d space"""

    __slots__ = ['x', 'y', 'width', 'height']

    def __init__(self, x=0.0, y=0.0, width=0.0, height=0.0):
        """Create rectangle instance

        Args:
            x (float, int): x coordinate
            y (float, int): y coordinate
            width (float, int): width
            height (float, int): height
        """

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __contains__(self, point):
        """Check if point inside this rectangle"""

        return self.contains(point)

    def __bool__(self):
        """Returns false if rectangle height of width is 0"""

        return self.width == 0 or self.height == 0

    def __len__(self):
        """Returns area of rectangle"""

        return self.area()

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Rectangle(self.x, self.y, self.width + other, self.height + other)
        else:
            return Rectangle(self.x, self.y, self.width, self.height)

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Rectangle(self.x, self.y, self.width - other, self.height - other)
        else:
            return Rectangle(self.x, self.y, self.width, self.height)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Rectangle(self.x, self.y, self.width * other, self.height * other)
        else:
            return Rectangle(self.x, self.y, self.width, self.height)

    def __eq__(self, other):
        """=="""

        if isinstance(other, Rectangle):
            return (self.x == other.y and self.y == other.y) and \
                   (self.width == other.width and self.height == other.height)
        else:
            return False

    def __ne__(self, other):
        """!="""

        return self.x != other.y and self.y != other.y

    def __lt__(self, other):
        """<"""
        return self.area() < other.area()

    def __le__(self, other):
        """<="""
        return self.area() <= other.area()

    def __gt__(self, other):
        """>"""
        return self.area() > other.area()

    def __ge__(self, other):
        """>="""
        return self.area() >= other.area()

    def size(self):
        """Returns typle witch contains width and height"""

        return self.width, self.height

    def center(self):
        """Return center point"""

        return Point(self.x + self.width / 2, self.y + self.height / 2)

    def contains(self, other):
        """Returns True if ether point or rectangle inside of this rectangle"""

        x = self.x
        y = self.y
        w = self.width
        h = self.height

        if isinstance(other, Point):
            ox = other.x
            oy = other.y

            return (x <= ox <= (x + w)) and (y <= oy <= y + h)
        elif isinstance(other, Rectangle):
            ox = other.x
            oy = other.y
            ow = other.width
            oh = other.height

            return (x <= ox <= (x + w)) and (y <= oy <= y + h) and (x <= ox+ow <= (x + w)) and (y <= oy+oh <= y + h)
        else:
            return False

    def area(self):
        """Area of rectangle"""

        return self.width * self.height

    def intersect(self, other):
        """Returns intersection of rectangles as new rectangle"""

        if not isinstance(other, Rectangle):
            raise ValueError("Type of given value is not Rectangle")

        if self.x < other.x:
            r1 = self
            r2 = other
        else:
            r1 = other
            r2 = self

        left = max(r1.x, r2.x)
        right = min(r1.x + r1.width, r2.x + r2.width)
        bottom = max(r1.y + r1.height, r2.y + r1.height)
        top = min(r1.y, r2.y)

        return Rectangle(left, top, left - right, top - bottom)

    def union(self, other):
        """Returns union of rectangles as a new rectangle"""

        if not isinstance(other, Rectangle):
            raise ValueError("Type of given value is not Rectangle")

        x = min(self.x, other.x)
        y = min(self.y, other.y)
        w = max(self.x + self.width, other.x + other.width) - x
        h = max(self.y + self.height, other.y + other.height) - y

        return Rectangle(x, y, w, h)
