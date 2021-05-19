import math

class Num3(object):
    def __init__(self, x=0, y=0, z=0):
        super(Num3, self).__init__()

        self.x = x
        self.y = y
        self.z = z


    def to_coords(self):
        return self.x, self.y, self.z
    
    @classmethod
    def from_str(cls, s):
        return cls(*eval(s))

    def to_dict(self):
        return {"x": self.x, "y": self.y, "z": self.z}

    @classmethod
    def from_dict(cls, dct):
        return cls(**dct)


    def __bool__(self):
        return self.x != 0 or self.y != 0 or self.z != 0

    def __eq__(self, other):
        try:
            return self.x == other.x and self.y == other.y and self.z == other.z
        except: pass
        try: 
            return self.x == other.x and self.y == other.y and self.z == 0
        except: pass
        return self.x == other and self.y == other and self.z == other
    
    def __add__(self, other):
        try:
            return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)
        except: pass
        try: 
            return self.__class__(self.x + other.x, self.y + other.y, self.z)
        except: pass
        return self.__class__(self.x + other, self.y + other, self.z + other)
    
    def __sub__(self, other):
        try:
            return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)
        except: pass
        try: 
            return self.__class__(self.x - other.x, self.y - other.y, self.z)
        except: pass
        return self.__class__(self.x - other, self.y - other, self.z - other)
    
    def __mul__(self, other):
        try:
            return self.__class__(self.x * other.x, self.y * other.y, self.z * other.z)
        except: pass
        try: 
            return self.__class__(self.x * other.x, self.y * other.y, self.z)
        except: pass
        return self.__class__(self.x * other, self.y * other, self.z * other)
    
    def __truediv__(self, other):
        try:
            return self.__class__(self.x / other.x, self.y / other.y, self.z / other.z)
        except: pass
        try: 
            return self.__class__(self.x / other.x, self.y / other.y, self.z)
        except: pass
        return self.__class__(self.x / other, self.y / other, self.z / other)
    
    def __floordiv__(self, other):
        try:
            return self.__class__(self.x // other.x, self.y // other.y, self.z // other.z)
        except: pass
        try: 
            return self.__class__(self.x // other.x, self.y // other.y, self.z)
        except: pass
        return self.__class__(self.x // other, self.y // other, self.z // other)
        
    def __mod__(self, other):
        try:
            return self.__class__(self.x % other.x, self.y % other.y, self.z % other.z)
        except: pass
        try: 
            return self.__class__(self.x % other.x, self.y % other.y, self.z)
        except: pass
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

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
