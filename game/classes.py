import math

from game import constants


class Worldpos(Pos3):
    def __init__(self, *args, **kwargs):
        super(Worldpos, self).__init__(*args, **kwargs)
    
    def to_screenpos(self, playerpos):
        return Screenpos(self.x - playerpos.x + constants.SCREEN_WIDTH // 2, self.y - playerpos.y + constants.SCREEN_HEIGHT // 2)


class Screenpos(object):
    def __init__(self, *args, **kwargs):
        super(Screenpos, self).__init__(*args, **kwargs)
    
    @classmethod
    def from_worldcoords(cls, x, y, playerpos):
        return Worldpos(x, y, 0).to_screenpos(playerpos)




class Pos2(object):
    def __init__(self, x=0.0, y=0.0):
        super(Pos2, self).__init__()

        self.x = x
        self.y = y


    def __bool__(self):
        return self.x != 0 or self.y != 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Pos3(object):
        def __init__(self, x=0.0, y=0.0, z=0):
        super(Pos2, self).__init__()

        self.x = x
        self.y = y
        self.z = z


    def __bool__(self):
        return self.x != 0 or self.y != 0 or self.z != 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __str__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.z})"


class Vector2(object):
    def __init__(self, x, y, *args, **kwargs):
        super(Vector2, self).__init__(*args, **kwargs)
        
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
        return f"{self.__class__.__name__}({self.x}, {self.y})"