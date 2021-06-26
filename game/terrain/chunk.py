import concurrent.futures

import pyglet

from game import debug, positions, constants
from .data_handler import load_chunk, write_chunk
from .tile import Tile


class Chunk(pyglet.event.EventDispatcher):
    def __init__(self, chunkpos):
        super(Chunk, self).__init__()
        
        self.register_event_type("on_update")

        self.chunkpos = chunkpos

        self.tiles = []

    
    def on_tile_update(self, tilepos):
        self.dispatch_event("on_update", self.chunkpos, tilepos)


    def set_pos(self, pos):
        screenpos = self.chunkpos.to_screenpos(pos)
        for col in self.tiles:
            for t in col:
                # TODO: Don't render if block above
                t.set_pos(screenpos, self.chunkpos.z - pos.z)

    async def load_tiles(self):
        # TODO: Needs optimizing
        chunk = load_chunk(self.chunkpos)

        # Turn the 3d-list of dicts -> 3d-list of Tiles
        self.tiles = list(map(lambda col: list(map(self.load_tile, col)), chunk))

    def load_tile(self, t_data):
        t = Tile.from_data(t_data)
        t.push_handlers(on_update=self.on_tile_update)
        return t

    def to_data(self):
        return list(map(lambda col: list(map(lambda t: t.to_data(), col)), self.tiles))

    def delete(self):
        try:
            for col in self.tiles:
                for t in col:
                    if t:
                        t.delete()
        except:
            debug.log("Error deleting chunk")

    def save(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(write_chunk, self.chunkpos, self.to_data())
