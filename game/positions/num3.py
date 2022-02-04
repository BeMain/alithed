import collections
import functools


@functools.total_ordering
class Num3(collections.namedtuple("Num3", "x y z")):
    @classmethod
    def from_str(cls, s):
        return cls(*eval(s))

    def __bool__(self):
        return self.x != 0 or self.y != 0 or self.z != 0

    def __eq__(self, other):
        try:
            return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)
        except:
            pass
        try:
            return (self.x == other.x) and (self.y == other.y) and (self.z == 0)
        except:
            pass
        return (self.x == other) and (self.y == other) and (self.z == other)

    def __lt__(self, other):
        try:
            return (self.x < other.x) and (self.y < other.y) and (self.z < other.z)
        except:
            return (self.x < other) and (self.y < other) and (self.z < other)

    def __gt__(self, other):
        try:
            return (self.x > other.x) and (self.y > other.y) and (self.z > other.z)
        except:
            return (self.x > other) and (self.y > other) and (self.z > other)

    def __neg__(self):
        return self.__class__(-self.x, -self.y, -self.z)

    def __add__(self, other):
        try:
            return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)
        except:
            pass
        try:
            return self.__class__(self.x + other.x, self.y + other.y, self.z)
        except:
            pass
        return self.__class__(self.x + other, self.y + other, self.z + other)

    def __sub__(self, other):
        try:
            return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)
        except:
            pass
        try:
            return self.__class__(self.x - other.x, self.y - other.y, self.z)
        except:
            pass
        return self.__class__(self.x - other, self.y - other, self.z - other)

    def __mul__(self, other):
        try:
            return self.__class__(self.x * other.x, self.y * other.y, self.z * other.z)
        except:
            pass
        try:
            return self.__class__(self.x * other.x, self.y * other.y, self.z)
        except:
            pass
        return self.__class__(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        try:
            return self.__class__(self.x / other.x, self.y / other.y, self.z / other.z)
        except:
            pass
        try:
            return self.__class__(self.x / other.x, self.y / other.y, self.z)
        except:
            pass
        return self.__class__(self.x / other, self.y / other, self.z / other)

    def __floordiv__(self, other):
        try:
            return self.__class__(self.x // other.x, self.y // other.y, self.z // other.z)
        except:
            pass
        try:
            return self.__class__(self.x // other.x, self.y // other.y, self.z)
        except:
            pass
        return self.__class__(self.x // other, self.y // other, self.z // other)

    def __mod__(self, other):
        try:
            return self.__class__(self.x % other.x, self.y % other.y, self.z % other.z)
        except:
            pass
        try:
            return self.__class__(self.x % other.x, self.y % other.y, self.z)
        except:
            pass
        return self.__class__(self.x % other, self.y % other, self.z % other)

    def __abs__(self):
        return self.__class__(abs(self.x), abs(self.y), abs(self.z))

    def __round__(self):
        return self.__class__(round(self.x), round(self.y), round(self.z))

    def __trunc__(self):
        return self.__class__(math.trunc(self.x), math.trunc(self.y), math.trunc(self.z))

    def __floor__(self):
        return self.__class__(math.floor(self.x), math.floor(self.y), math.floor(self.z))

    def __ceil__(self):
        return self.__class__(math.ceil(self.x), math.ceil(self.y), math.ceil(self.z))
