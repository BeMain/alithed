import math
import numpy as np
import time
import itertools

import pyglet
from pyglet.window import key

from game import constants, debug, util, classes
from game.terrain import chunk, data_handler


# TODO: Implement zooming in and out

class Terrain():
    instance = None

    class __Terrain(pyglet.event.EventDispatcher):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.register_event_type("on_update")
            
            self.corner_chunks = []
            self.chunks = {}

        def update(self, playerpos):
            self.set_pos(playerpos)

        def set_pos(self, pos):
            self.load_chunks_on_screen(pos)

            for chunk in self.chunks.values():
                screenpos = classes.Screenpos.from_worldcoords(chunk.chunk_x * constants.CHUNK_SIZE * constants.TILE_SIZE, chunk.chunk_y * constants.CHUNK_SIZE * constants.TILE_SIZE, pos)

                chunk.set_pos(screenpos.x, screenpos.y, pos.z)

        @debug.timeit
        def load_chunks_on_screen(self, pos):
            w = constants.SCREEN_WIDTH // 2
            h = constants.SCREEN_HEIGHT // 2

            # Get chunk positions for lower left and upper right corner corners
            corners = []
            for pair in [(-1, -1), (1, 1)]:
                corners.append(self.get_chunkpos_at(pair[0] * w + pos.x, pair[1] * h + pos.y))
            self.corner_chunks = corners

            old_keys = self.chunks.keys() if self.chunks else []
            # Get positions for chunks on screen
            new_keys = []
            for x in range(corners[0][0], corners[1][0] + 1):
                for y in range(corners[0][1], corners[1][1] + 1):
                    for z in range(pos.z - 1, pos.z + 2):
                        new_keys.append((x, y, z))

            # Load new chunks
            for chunkx, chunky, chunkz in new_keys:
                if (chunkx, chunky, chunkz) not in self.chunks.keys():
                    debug.log(f"loading {(chunkx, chunky, chunkz)}")
                    self.load_chunk(chunkx, chunky, chunkz)

            # Unload old chunks
            to_remove = list(set(old_keys) - set(new_keys))
            for key in to_remove:
                debug.log(f"unloading {(key[0], key[1], key[2])}")
                self.unload_chunk(key)
                            
                        
        def load_chunk(self, chunkx, chunky, chunkz):
            c = chunk.Chunk(chunkx, chunky, chunkz)
            c.push_handlers(on_update=self.on_tile_update)
            self.chunks[(chunkx, chunky, chunkz)] = c

        def unload_chunk(self, key):
            self.chunks[key].save()
            self.chunks[key].delete()
            del self.chunks[key]

        def get_chunkpos_at(self, worldx, worldy):
            chunkx = int((worldx + constants.TILE_SIZE / 2) // (constants.TILE_SIZE * constants.CHUNK_SIZE))
            chunky = int((worldy + constants.TILE_SIZE / 2) // (constants.TILE_SIZE * constants.CHUNK_SIZE))
            return chunkx, chunky


        def on_tile_update(self, chunk_x, chunk_y, chunk_z, tile_x, tile_y):
            self.dispatch_event("on_update", chunk_x, chunk_y, chunk_z, tile_x, tile_y)

        def get_tile(self, world_x, world_y, z):
            chunk_x, chunk_y = self.get_chunkpos_at(world_x, world_y)

            tile_x = int(round((world_x) % (constants.CHUNK_SIZE * constants.TILE_SIZE) / constants.TILE_SIZE))
            tile_y = int(round((world_y) % (constants.CHUNK_SIZE * constants.TILE_SIZE) / constants.TILE_SIZE))

            # Make sure the value is within bounds
            if tile_x == constants.CHUNK_SIZE: tile_x = 0
            if tile_y == constants.CHUNK_SIZE: tile_y = 0

            # Check if requested chunk is loaded
            if (chunk_x, chunk_y, z) in self.chunks.keys():
                # Just grab the correct chunk
                c = self.chunks[(chunk_x, chunk_y, z)]
            else:
                # Load the chunk from memory
                c = chunk.Chunk(chunk_x, chunk_y, z)
            
            tile = c.tiles[tile_x][tile_y]
            return tile


    def __init__(self, *args, **kwargs):
        if not Terrain.instance:
            Terrain.instance = Terrain.__Terrain(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.instance, name)
