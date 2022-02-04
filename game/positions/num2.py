import collections
import functools


@functools.total_ordering
class Num2(collections.namedtuple("Num2", "x y")):
    def __bool__(self):
        return self.x != 0 or self.y != 0

    def __eq__(self, other):
        try:
            return (self.x == other.x) and (self.y == other.y)
        except:
            return (self.x == other) and (self.y == other)

    def __lt__(self, other):
        try:
            return (self.x < other.x) and (self.y < other.y)
        except:
            return (self.x < other) and (self.y < other)

    def __gt__(self, other):
        try:
            return (self.x > other.x) and (self.y > other.y)
        except:
            return (self.x > other) and (self.y > other)

    def __neg__(self):
        return self.__class__(-self.x, -self.y)

    def __add__(self, other):
        try:
            return self.__class__(self.x + other.x, self.y + other.y)
        except:
            return self.__class__(self.x + other, self.y + other)

    def __sub__(self, other):
        try:
            return self.__class__(self.x - other.x, self.y - other.y)
        except:
            return self.__class__(self.x - other, self.y - other)

    def __mul__(self, other):
        try:
            return self.__class__(self.x * other.x, self.y * other.y)
        except:
            return self.__class__(self.x * other, self.y * other)

    def __truediv__(self, other):
        try:
            return self.__class__(self.x / other.x, self.y / other.y)
        except:
            return self.__class__(self.x / other, self.y / other)

    def __floordiv__(self, other):
        try:
            return self.__class__(self.x // other.x, self.y // other.y)
        except:
            return self.__class__(self.x // other, self.y // other)

    def __mod__(self, other):
        try:
            return self.__class__(self.x % other.x, self.y % other.y)
        except:
            return self.__class__(self.x % other, self.y % other)

    def __abs__(self):
        return self.__class__(abs(self.x), abs(self.y))

    def __round__(self):
        return self.__class__(round(self.x), round(self.y))

    def __trunc__(self):
        return self.__class__(math.trunc(self.x), math.trunc(self.y))

    def __floor__(self):
        return self.__class__(math.floor(self.x), math.floor(self.y))

    def __ceil__(self):
        return self.__class__(math.ceil(self.x), math.ceil(self.y))
