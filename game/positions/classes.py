import math

from game import constants
from game.positions import num2, num3


class Pos2(num2.Num2):
    def clamp(self, minpos, maxpos):
        self.x = max(min(self.x, maxpos.x), minpos.x)
        self.y = max(min(self.y, maxpos.y), minpos.y)

    def loop_around(self, maxpos):
        if self.x >= maxpos.x:
            self.x %= maxpos.x
        if self.y >= maxpos.y:
            self.y %= maxpos.y

    def distancesq_to(self, pos):
        return (self.x - pos.x)**2 + (self.y - pos.y)**2

    def angle_to(self, pos):
        x = self.x - pos.x
        y = self.y - pos.y
        return -math.degrees(math.atan2(y, x))

    @classmethod
    def from_pos2(cls, pos2):
        return cls(*pos2.to_coords())

    @classmethod
    def from_pos3(cls, pos3):
        return cls(*pos3.to_coords()[0:2])


class Pos3(num3.Num3):
    def clamp(self, minpos, maxpos):
        self.x = max(min(self.x, maxpos.x), minpos.x)
        self.y = max(min(self.y, maxpos.y), minpos.y)
        self.z = max(min(self.z, maxpos.z), minpos.z)

    @classmethod
    def from_pos2(cls, pos2, z):
        return cls(*pos2.to_coords(), z)

    @classmethod
    def from_pos3(cls, pos3):
        return cls(*pos3.to_coords())


class Size2(num2.Num2):
    @property
    def width(self):
        return self.x

    @property
    def height(self):
        return self.y

    @classmethod
    def tilesize(cls):
        return cls(constants.TILE_SIZE, constants.TILE_SIZE)

    @classmethod
    def chunk_tiles(cls):
        return cls(constants.CHUNK_SIZE, constants.CHUNK_SIZE)

    @classmethod
    def chunksize(cls):
        size = constants.TILE_SIZE * constants.CHUNK_SIZE
        return cls(size, size)

    @classmethod
    def screensize(cls):
        return cls(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)


class Vector2(num2.Num2):
    def normalize(self, precision=3):
        v = math.atan2(self.y, self.x)
        self.x = round(math.cos(v), precision)
        self.y = round(math.sin(v), precision)
