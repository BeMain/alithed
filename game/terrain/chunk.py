import concurrent.futures

import pyglet

from game import wraps
from game.terrain import data_handler, terrain_generation, terrain, tile


class Chunk(pyglet.event.EventDispatcher):
    def __init__(self, chunk_x, chunk_y, chunk_z, *args, **kwargs):
        super(Chunk, self).__init__(*args, **kwargs)
        
        self.register_event_type("on_update")

        self.chunk_x = chunk_x
        self.chunk_y = chunk_y
        self.chunk_z = chunk_z

        self.tiles = []
        self.load_tiles()

    
    def on_tile_update(self, tile_x, tile_y):
        self.dispatch_event("on_update", self.chunk_x, self.chunk_y, self.chunk_z, tile_x, tile_y)

    def set_pos(self, x, y, z):
        if z < 0:
            c_above = terrain.Terrain().chunks[(self.chunk_x, self.chunk_y, self.chunk_z + 1)]
        for col in self.tiles:
            for tile in col:
                # Don't render tile if block above
                if z < 0 and c_above.tiles[tile.tile_x][tile.tile_y].material != "air":
                    tile.batch = None

                tile.set_pos(x, y, z)

    def load_tiles(self):
        # TODO: Needs optimizing
        chunk = data_handler.load_chunk(self.chunk_x, self.chunk_y, self.chunk_z)

        # Turn the 3d-list of dicts -> 3d-list of Tiles
        self.tiles = list(map(lambda col: list(map(self.load_tile, col)), chunk))

    def load_tile(self, t_data):
        t = tile.Tile.from_data(t_data)
        t.push_handlers(on_update=self.on_tile_update)
        return t

    def to_data(self):
        return list(map(lambda col: list(map(lambda tile: tile.to_data(), col)), self.tiles))

    def delete(self):
        for col in self.tiles:
            for tile in col:
                if tile:
                    tile.delete()

    def save(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(data_handler.write_chunk, self.chunk_x, self.chunk_y, self.chunk_z, self.to_data())
