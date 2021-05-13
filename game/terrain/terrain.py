import math
import numpy as np
import time
import itertools

import pyglet
from pyglet.window import key

from game import constants, debug, positions
from game.terrain import chunk, data_handler


# TODO: Implement zooming in and out

class Terrain():
    instance = None

    class __Terrain(pyglet.event.EventDispatcher):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.register_event_type("on_update")
            
            self.chunks = {}

        def update(self, playerpos):
            self.set_pos(playerpos)

        def set_pos(self, pos):
            self.load_chunks_on_screen(pos)

            for chunk in self.chunks.values():
                chunk.set_pos(pos)

        @debug.timeit
        def load_chunks_on_screen(self, pos):
            w = constants.SCREEN_WIDTH // 2
            h = constants.SCREEN_HEIGHT // 2

            # Get chunk positions for lower left and upper right corner corners
            corners = []
            for rel_cords in [(-1, -1), (1, 1)]:
                x, y = self.get_chunkpos_at(rel_cords[0] * w + pos.x, rel_cords[1] * h + pos.y)
                corners.append(positions.Chunkpos(x, y, 0))

            old_keys = self.chunks.keys() if self.chunks else []
            # Get positions for chunks on screen
            new_keys = []
            for x in range(corners[0].x, corners[1].x + 1):
                for y in range(corners[0].y, corners[1].y + 1):
                    for z in range(pos.z - 1, pos.z + 2):
                        new_keys.append(str((x, y, z)))

            # Load new chunks
            for key in new_keys:
                if key not in self.chunks.keys():
                    debug.log(f"loading {key}")
                    self.load_chunk(positions.Chunkpos.from_str(key))

            # Unload old chunks
            to_remove = list(set(old_keys) - set(new_keys))
            for key in to_remove:
                debug.log(f"unloading {key}")
                self.unload_chunk(positions.Chunkpos.from_str(key))
                            
                        
        def load_chunk(self, chunkpos):
            c = chunk.Chunk(chunkpos)
            c.push_handlers(on_update=self.on_tile_update)
            self.chunks[str(chunkpos)] = c

        def unload_chunk(self, chunkpos):
            self.chunks[str(chunkpos)].save()
            self.chunks[str(chunkpos)].delete()
            del self.chunks[str(chunkpos)]

        def get_chunkpos_at(self, worldx, worldy):
            chunkx = int((worldx + constants.TILE_SIZE / 2) // (constants.TILE_SIZE * constants.CHUNK_SIZE))
            chunky = int((worldy + constants.TILE_SIZE / 2) // (constants.TILE_SIZE * constants.CHUNK_SIZE))
            return chunkx, chunky


        def on_tile_update(self, chunkpos, tilepos):
            self.dispatch_event("on_update", chunkpos, tilepos)

        def get_tile(self, x, y, z):
            worldpos = positions.Worldpos(x, y, z)
            chunkpos = worldpos.to_chunkpos()

            tile_x = int(round((worldpos.x) % (constants.CHUNK_SIZE * constants.TILE_SIZE) / constants.TILE_SIZE))
            tile_y = int(round((worldpos.y) % (constants.CHUNK_SIZE * constants.TILE_SIZE) / constants.TILE_SIZE))

            # Make sure the value is within bounds
            if tile_x == constants.CHUNK_SIZE: tile_x = 0
            if tile_y == constants.CHUNK_SIZE: tile_y = 0

            # Check if requested chunk is loaded
            try:
                # Just grab the correct chunk
                c = self.chunks[str(chunkpos)]
            except:
                # Load the chunk from memory
                c = chunk.Chunk(chunkpos)
            
            tile = c.tiles[tile_x][tile_y]
            return tile


    def __init__(self, *args, **kwargs):
        if not Terrain.instance:
            Terrain.instance = Terrain.__Terrain(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.instance, name)
