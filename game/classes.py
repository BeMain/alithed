import math


class Pos2(object):
    def __init__(self, x=0.0, y=0.0):
        super(Pos2, self).__init__()

        self.x = x
        self.y = y


    def clamp(self, minpos, maxpos):
        self.x = max(min(self.x, maxpos.x), minpos.x)
        self.y = max(min(self.y, maxpos.y), minpos.y)
    
    def distancesq_to(self, pos):
        return (self.x - pos.x)**2 + (self.y - pos.y)**2
    
    def angle_to(self, pos):
        x = self.x - pos.x
        y = self.y - pos.y
        return -math.degrees(math.atan2(y, x))


    def to_coords(self):
        return self.x, self.y
    
    def to_list(self):
        return [self.x, self.y]

    @classmethod
    def from_list(cls, lst):
        return cls(*lst)

    def to_dict(self):
        return {"x": self.x, "y": self.y}

    @classmethod
    def from_dict(cls, dct):
        return cls(**dct)


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
        super(Pos3, self).__init__()

        self.x = x
        self.y = y
        self.z = z


    def clamp(self, minpos, maxpos):
        self.x = max(min(self.x, maxpos.x), minpos.x)
        self.y = max(min(self.y, maxpos.y), minpos.y)
        self.z = max(min(self.z, maxpos.z), minpos.z)


    def to_coords(self):
        return self.x, self.y, self.z
    
    def to_list(self):
        return [self.x, self.y, self.z]

    @classmethod
    def from_list(cls, lst):
        return cls(*lst)

    def to_dict(self):
        return {"x": self.x, "y": self.y, "z": self.z}

    @classmethod
    def from_dict(cls, dct):
        return cls(**dct)


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

