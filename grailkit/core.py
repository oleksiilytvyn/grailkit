# -*- coding: UTF-8 -*-
"""
    grailkit.core
    ~~~~~~~~~~~~~

    Core types and widely used components

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
import math
import weakref


class Signal(object):
    """Callback mechanism for DNA
    This class uses weak references to callbacks so methods can be deleted
    if no references exists"""

    def __init__(self, *args):
        """Create signal

        Args:
            *args: template of arguments
        """

        self._args = [type(x) for x in args]
        self._fns = {}
        self._flush_keys = []

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

        ref = self._wrap(fn)

        if not name:
            name = len(self._fns)

        self._fns[name] = ref

    def disconnect(self, fn):
        """Remove function from list, if it previously added to it

        Args:
            fn (callable): function to remove
        """

        found_key = None

        for key, value in self._fns.items():
            if value[0] and fn == value[1]():
                found_key = key

                break

        if found_key:
            del self._fns[found_key]

    def emit(self, *args, name=False, **kwargs):
        """Emit signal
        If `name` argument was given, only slot with this name will be called
        otherwise all slots will be called

        Args:
            *args: arguments to pass to callbacks
            name (str): give name of slot to be called
        """

        if name and name in self._fns:
            return self._call(name, *args, **kwargs)

        for key in self._fns:
            self._call(key, *args, **kwargs)

        # remove dead references
        self._flush()

    def _wrap(self, fn):
        """Returns typle with parent object and method"""

        if hasattr(fn, '__self__'):
            return weakref.ref(fn.__self__), weakref.ref(fn.__func__)
        else:
            return None, fn

    def _call(self, name, *args, **kwargs):
        """Call method, if reference is dead flush"""

        ref = self._fns[name]
        obj = ref[0]
        fun = ref[1]

        # bound
        if callable(obj) and obj() and callable(fun):
            callback = getattr(obj(), fun().__name__)
            callback(*args, **kwargs)
        # unbound
        elif obj is None and fun:
            fun(*args, **kwargs)
        # non exists
        else:
            self._flush_keys.append(name)

    def _flush(self):

        for key in set(self._flush_keys):
            if key in self._fns:
                del self._fns[key]

        self._flush_keys = []


class Signalable(object):
    """Like a Signal but with messages and bundles"""
    # todo: implement this using weakref module

    def __init__(self):

        self.__slots = {}
        self.__bundle_slots = []

    def __bool__(self):
        """Returns True"""

        return True

    def __len__(self):
        """Returns number of registered callbacks"""

        return sum(len(v) for k, v in self.__slots.items()) + len(self.__bundle_slots)

    def connect(self, message, fn):
        """Connect listener `fn` to slot `message`

        Args:
            message (str): slot name
            fn (callable): function to call
        Raises:
            ValueError if at least one of arguments is not supported
        """

        if not isinstance(message, str):
            raise ValueError("Can't connect to slot '%s', given value is not of type string" % message)

        if not callable(fn):
            raise ValueError("Given function is not callable.")

        if message not in self.__slots:
            self.__slots[message] = []

        self.__slots[message].append(fn)

    def disconnect(self, message, fn):
        """Disconnect listener from slot

        Args:
            message (str): slot name
            fn (callable): function to call
        """

        if message in self.__slots:
            self.__slots[message].remove(fn)

    def emit(self, message, *args):
        """Trigger all listeners of message

        Args:
            message (str): slot name
            *args: list of arguments
        """
        if message in self.__slots:
            for fn in self.__slots[message]:
                fn(*args)

    def connect_bundle(self, fn):
        """Connect a bundle listener"""

        if not callable(fn):
            raise ValueError("Given function is not callable.")

        if fn not in self.__bundle_slots:
            self.__bundle_slots.append(fn)

    def disconnect_bundle(self, fn):
        """Remove bundle listener"""

        if fn in self.__bundle_slots:
            self.__bundle_slots.remove(fn)

    def emit_bundle(self, bundle):
        """Emit bundle of messages"""

        for fn in self.__bundle_slots:
            fn(bundle)


class Color(object):
    """Color representation"""

    __slots__ = ['r', 'g', 'b', 'a']

    def __init__(self, r=0.0, g=0.0, b=0.0, a=1.0):
        """Create color

        Args:
            r (float, int): Red value
            g (float, int): Green value
            b (float, int): Blue value
            a (float, int): Opacity value
        """
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def to_hex(self):
        """Returns color in RGB hex format"""

        return '#%02x%02x%02x' % (self.r, self.g, self.b)

    def to_hex_rgba(self):
        """Returns color in RGBA hex format"""

        return '#%02x%02x%02x%02x' % (self.r, self.g, self.b, self.a)

    @staticmethod
    def from_hex(value):
        """Create color instance from rgb hex string

        Args:
            value (str): rgb color in hex format
        """

        if value[0] == '#':
            value = value[1:]

        r = 0.0
        g = 0.0
        b = 0.0
        a = 0.0

        if len(value) == 3:
            r = int(value[:1]*2, 16)
            g = int(value[1:2]*2, 16)
            b = int(value[2:3]*2, 16)
        elif len(value) == 6:
            r = int(value[:2], 16)
            g = int(value[2:4], 16)
            b = int(value[4:6], 16)
        elif len(value) == 8:
            r = int(value[:2], 16)
            g = int(value[2:4], 16)
            b = int(value[4:6], 16)
            a = int(value[6:8], 16)

        return Color(r, g, b, a)


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
