import collections
import functools


@functools.total_ordering
class Num2(collections.namedtuple("Num2", "x y")):
    def __gt__(self, other):
        return (self.x > other.x) and (self.y > other.y)


@functools.total_ordering
class Num3(collections.namedtuple("Num3", "x y z")):
    def __gt__(self, other):
        return (self.x > other.x) and (self.y > other.y) and (self.z > other.z)
