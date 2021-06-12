import concurrent.futures
import numpy as np

import pyglet

from game import debug, constants
from game.positions import Size2
from game.terrain import data_handler
from .tile import Tile


class Chunk(pyglet.event.EventDispatcher):
    def __init__(self, chunkpos):
        super(Chunk, self).__init__()
        
        self.register_event_type("on_update")

        self.chunkpos = chunkpos

        self.tiles = np.zeros(constants.CHUNK_SIZE ** 2)
        self._load_tiles()

    
    def on_tile_update(self, tilepos):
        self.dispatch_event("on_update", self.chunkpos, tilepos)


    def get_tile(self, tilepos):
        return self.tiles[tilepos.to_index()]

    def set_pos(self, pos):
        screenpos = self.chunkpos.to_screenpos(pos)
        for tile in self.tiles:
            # TODO: Don't render if block above
            tile.set_pos(screenpos, self.chunkpos.z - pos.z)

    def _load_tiles(self):
        # TODO: Needs optimizing
        chunk = data_handler.load_chunk(self.chunkpos)

        # Turn the 3d-list of dicts -> 3d-list of Tiles
        self.tiles = np.array([self._load_tile(tile) for tile in chunk])

    def _load_tile(self, t_data):
        tile = Tile.from_data(t_data)
        tile.push_handlers(on_update=self.on_tile_update)
        return tile

    def to_data(self):
        return [tile.to_data() for tile in self.tiles]

    def delete(self):
        try:
            for tile in self.tiles:
                if tile:
                    tile.delete()
        except:
            debug.log("Error deleting chunk")

    def save(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(data_handler.write_chunk, self.chunkpos, self.to_data())
