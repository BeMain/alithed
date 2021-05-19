from game import constants
from game.positions import classes


class Screenpos(classes.Pos2):
    def __init__(self, *args, **kwargs):
        super(Screenpos, self).__init__(*args, **kwargs)
    

    def clamp_to_screen(self):
        self.clamp(Screenpos(), classes.Size2.screensize())
    
    def is_on_screen(self, margin=0):
        return (self.x > -margin) and (self.x < constants.SCREEN_WIDTH + margin) and (self.y > -margin) and (self.y < constants.SCREEN_HEIGHT + margin)


    def to_worldpos(self, playerpos):
        return Worldpos(self.x + playerpos.x - constants.SCREEN_WIDTH // 2, self.y + playerpos.y - constants.SCREEN_HEIGHT // 2, playerpos.z)


    @classmethod
    def from_worldcoords(cls, x, y, playerpos):
        return Worldpos(x, y, 0).to_screenpos(playerpos)


class Worldpos(classes.Pos3):
    def __init__(self, *args, **kwargs):
        super(Worldpos, self).__init__(*args, **kwargs)
    
    def to_screenpos(self, playerpos):
        return Screenpos.from_pos3(self - playerpos) + classes.Size2.screensize() // 2
    
    def to_chunkpos(self):
        return round(Chunkpos.from_pos3((self + classes.Size2.tilesize() // 2) // classes.Size2.chunksize()))
    
    def to_tilepos(self):
        return round(Tilepos.from_pos3(self % classes.Size2.chunksize() / constants.TILE_SIZE))


class Chunkpos(classes.Pos3):
    def __init__(self, *args, **kwargs):
        super(Chunkpos, self).__init__(*args, **kwargs)
    
    def to_worldpos(self):
        return Worldpos.from_pos3(self * classes.Size2.chunksize())
    
    def to_screenpos(self, playerpos):
        return self.to_worldpos().to_screenpos(playerpos)


class Tilepos(classes.Pos2):
    def __init__(self, *args, **kwargs):
        super(Tilepos, self).__init__(*args, **kwargs)
    