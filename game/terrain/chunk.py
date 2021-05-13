import concurrent.futures

import pyglet

from game import debug, positions, constants
from game.terrain import data_handler, terrain_generation, terrain, tile


class Chunk(pyglet.event.EventDispatcher):
    def __init__(self, chunkpos):
        super(Chunk, self).__init__()
        
        self.register_event_type("on_update")

        self.chunkpos = chunkpos

        self.tiles = []
        self.load_tiles()

    
    def on_tile_update(self, tilepos):
        self.dispatch_event("on_update", self.chunkpos, tilepos)


    def set_pos(self, pos):
        screenpos = self.chunkpos.to_screenpos(pos)
        for col in self.tiles:
            for tile in col:
                # TODO: Don't render if block above
                tile.set_pos(screenpos, self.chunkpos.z - pos.z)

    def load_tiles(self):
        # TODO: Needs optimizing
        chunk = data_handler.load_chunk(self.chunkpos)

        # Turn the 3d-list of dicts -> 3d-list of Tiles
        self.tiles = list(map(lambda col: list(map(self.load_tile, col)), chunk))

    def load_tile(self, t_data):
        t = tile.Tile.from_data(t_data)
        t.push_handlers(on_update=self.on_tile_update)
        return t

    def to_data(self):
        return list(map(lambda col: list(map(lambda tile: tile.to_data(), col)), self.tiles))

    def delete(self):
        try:
            for col in self.tiles:
                for tile in col:
                    if tile:
                        tile.delete()
        except:
            debug.log("Error deleting chunk")

    def save(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(data_handler.write_chunk, self.chunkpos, self.to_data())
