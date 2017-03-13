# -*- coding: UTF-8 -*-
"""
    grailkit.core
    ~~~~~~~~~~~~~

    Core types and widely used components

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
import math


class Signal(object):
    """Callback mechanism for DNA"""

    def __init__(self, *args):
        """Create signal

        Args:
            *args: template of arguments
        """

        self._args = [type(x) for x in args]
        self._fns = {}

    def __len__(self):
        """Returns number of connected slots"""

        return len(self._fns)

    def __bool__(self):
        """Returns True and prevent from converting to False when number of slots 0"""

        return True

    def connect(self, fn, name=False):
        """Add function to list of callbacks

        Args:
            fn (callable): function to call on emit
            name (str): give name to slot
        """

        if not callable(fn):
            raise ValueError("Given object is not callable")

        if not name:
            name = len(self._fns)

        self._fns[name] = fn

    def disconnect(self, fn):
        """Remove function from list, if it previously added to it

        Args:
            fn (callable): function to remove
        """

        ref = None

        for key in self._fns:
            if fn == self._fns[key]:
                ref = key
                break

        if ref:
            del self._fns[ref]

    def emit(self, *args, name=False):
        """Emit signal
        If `name` argument was given, only slot with this name will be called
        otherwise all slots will be called

        Args:
            *args: arguments to pass to callbacks
            name (str): give name of slot to be called
        """

        if name:
            if name in self._fns:
                self._fns[name](*args)

            return

        for key in self._fns:
            self._fns[key](*args)


class Color(object):
    """Color representation"""

    __slots__ = ['r', 'g', 'b', 'a']

    def __init__(self, r=0.0, g=0.0, b=0.0, a=1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def hex(self):
        """Returns color in RGB hex format"""

        return '#' + str([self.r, self.g, self.b])

    def hex_rgba(self):
        """Returns color in RGBA hex format"""

        return '#' + str([self.r, self.g, self.b, self.a])


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


class Rect(Point):
    """2d rectangle in 2d space"""

    __slots__ = ['x', 'y', 'width', 'height']

    def __init__(self, x=0.0, y=0.0, width=0.0, height=0.0):
        super(Rect, self).__init__(x, y)

        self.width = width
        self.height = height

    def __contains__(self, point):
        return self.contains(point)

    def center(self):
        """Return center point"""

        return Point(self.x + self.width / 2, self.y + self.height / 2)

    def contains(self, point):
        """Returns weather point in rect"""

        return (self.x <= point.x <= self.x + self.width) and (self.y <= point.y <= self.y + self.height)

    def area(self):
        """Area of square"""

        return self.width * self.height

    def intersect(self, other):
        """Returns intersection of rectangles as new rectangle"""

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

        return Rect(left, top, left - right, top - bottom)

    def union(self, other):
        """Returns union of rectangles as new rectangle"""

        x = min(self.x, other.x)
        y = min(self.y, other.y)
        w = max(self.x + self.width, other.x + other.width) - x
        h = max(self.y + self.height, other.y + other.height) - y

        return Rect(x, y, w, h)
