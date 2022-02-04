import collections
import math


Num2 = collections.namedtuple("Num2", "x y")
Num3 = collections.namedtuple("Num3", Num2._fields + ("z",))

Size2 = collections.namedtuple("Size2", "width, height")


class Pos2(Num2):
    @classmethod
    def from_pos2(cls, pos2):
        return cls(*pos2)

    @classmethod
    def from_pos3(cls, pos3):
        return cls(*pos3[0:2])

    def clamped(self, minpos, maxpos):
        newx = max(min(self.x, maxpos.x), minpos.x)
        newy = max(min(self.y, maxpos.y), minpos.y)
        return self._replace(x=newx, y=newy)

    def distancesq_to(self, pos):
        return (self.x - pos.x)**2 + (self.y - pos.y)**2

    def angle_to(self, pos):
        x = self.x - pos.x
        y = self.y - pos.y
        return -math.degrees(math.atan2(y, x))

    def __mod__(self, pos):
        return self._replace(x=self.x % pos.x, y=self.y % pos.y)


class Pos3(Num3):
    @classmethod
    def from_pos2(cls, pos2, z):
        return cls(*pos2, z=z)

    @classmethod
    def from_pos3(cls, pos3):
        return cls(*pos3)

    def clamped(self, minpos, maxpos):
        newx = max(min(self.x, maxpos.x), minpos.x)
        newy = max(min(self.y, maxpos.y), minpos.y)
        newz = max(min(self.z, maxpos.z), minpos.z)
        return self._replace(x=newx, y=newy, z=newz)

    def distancesq_to(self, pos):
        return (self.x - pos.x)**2 + (self.y - pos.y)**2 + (self.z - pos.z)**2

    def __mod__(self, pos):
        return self._replace(x=self.x % pos.x, y=self.y % pos.y)


class Vector2(Num2):
    def normalized(self, precision=3):
        v = math.atan2(self.y, self.x)
        newx = round(math.cos(v), precision)
        newy = round(math.sin(v), precision)
        return self._replace(x=newx, y=newy)
