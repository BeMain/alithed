import math

from game import constants


class Vector(object):
    def __init__(self, x, y, *args, **kwargs):
        super(Vector, self).__init__(*args, **kwargs)
        
        self.x = x
        self.y = y
    
    @classmethod
    def ZERO(cls):
        return cls(0.0, 0.0)
    
    def normalize(self, precision=3):
        v = math.atan2(self.y, self.x)
        self.x = round(math.cos(v), precision)
        self.y = round(math.sin(v), precision)

    
    def __bool__(self):
        return self.x != 0 or self.y != 0

    def __str__(self):
        return f"Vector({self.x}, {self.y})"


class Worldpos(object):
    def __init__(self, x=0.0, y=0.0, z=0):
        super(Worldpos, self).__init__()

        self.x = x
        self.y = y
        self.z = z
    
    def to_screenpos(self, playerpos):
        return Screenpos(self.x - playerpos.x + constants.SCREEN_WIDTH // 2, self.y - playerpos.y + constants.SCREEN_HEIGHT // 2)


    def __bool__(self):
        return self.x != 0 or self.y != 0 or self.z != 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __add__(self, other):
        return Worldpos(self.x + other.x, self.y + other.y, self.z + other.z)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


class Screenpos(object):
    def __init__(self, x=0.0, y=0.0):
        super(Screenpos, self).__init__()

        self.x = x
        self.y = y


    def __bool__(self):
        return self.x != 0 or self.y != 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other):
        return Worldpos(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"({self.x}, {self.y})"
    
    @classmethod
    def from_worldcoords(cls, x, y, playerpos):
        return Worldpos(x, y, 0).to_screenpos(playerpos)