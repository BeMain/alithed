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


def clamp(my_value, min_value, max_value):
    return max(min(my_value, max_value), min_value)

def distancesq(pos1, pos2):
    return (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2

def angle_between(pos1, pos2):
    x = pos1[0] - pos2[0]
    y = pos1[1] - pos2[1]
    return -math.degrees(math.atan2(y, x))


def to_screenpos(worldpos, playerpos):
    x = worldpos[0] - playerpos[0] + constants.SCREEN_WIDTH // 2
    y = worldpos[1] - playerpos[1] + constants.SCREEN_HEIGHT // 2
    return (x, y)
