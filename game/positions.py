from game import constants, classes


class Screenpos(classes.Pos2):
    def __init__(self, *args, **kwargs):
        super(Screenpos, self).__init__(*args, **kwargs)
    
    @classmethod
    def from_worldcoords(cls, x, y, playerpos):
        return Worldpos(x, y, 0).to_screenpos(playerpos)


class Worldpos(classes.Pos3):
    def __init__(self, *args, **kwargs):
        super(Worldpos, self).__init__(*args, **kwargs)
    
    def to_screenpos(self, playerpos):
        return Screenpos(self.x - playerpos.x + constants.SCREEN_WIDTH // 2, self.y - playerpos.y + constants.SCREEN_HEIGHT // 2)


class Chunkpos(classes.Pos3):
    def __init__(self, *args, **kwargs):
        super(Chunkpos, self).__init__(*args, **kwargs)
    
    def to_worldpos(self):
        return Worldpos(self.x * constants.CHUNK_SIZE * constants.TILE_SIZE, self.y * constants.CHUNK_SIZE * constants.TILE_SIZE, self.z)
    
    def to_screenpos(self, playerpos):
        return self.to_worldpos().to_screenpos(playerpos)


class Tilepos(classes.Pos2):
    def __init__(self, *args, **kwargs):
        super(Tilepos, self).__init__(*args, **kwargs)
    