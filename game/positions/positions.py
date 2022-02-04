from game import constants
from game.positions import Pos2, Pos3


class Screenpos(Pos2):
    def clamp_to_screen(self):
        self.clamp(self, constants.SCREEN_SIZE)

    def is_on_screen(self, margin=Pos2(0, 0)):
        return (self > -margin) and (self < constants.SCREEN_SIZE + margin)

    def to_worldpos(self, playerpos):
        return Worldpos.from_pos3(playerpos + self - constants.SCREEN_SIZE // 2)


class Worldpos(Pos3):
    def to_screenpos(self, playerpos):
        return Screenpos.from_pos3(self - playerpos) + constants.SCREEN_SIZE // 2

    def to_chunkpos(self):
        return round(Chunkpos.from_pos3((self + constants.TILE_SIZE // 2) // constants.CHUNK_SIZE))

    def to_tilepos(self):
        return round(Tilepos.from_pos3((self % constants.CHUNK_SIZE) / constants.TILE_SIZE))


class Chunkpos(Pos3):
    def to_worldpos(self):
        return Worldpos.from_pos3(self * constants.CHUNK_SIZE)

    def to_screenpos(self, playerpos):
        return self.to_worldpos().to_screenpos(playerpos)


class Tilepos(Pos2):
    @classmethod
    def from_index(cls, idx):
        return cls(idx // constants.CHUNK_N_TILES.width, idx % constants.CHUNK_N_TILES.height)

    def to_index(self):
        return self.y + self.x * constants.CHUNK_N_TILES.width
