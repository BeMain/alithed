import math
import numpy as np
import time
import itertools

import pyglet
from pyglet.window import key

from game import constants, wraps
from game.terrain import chunk, data_handler


# TODO: Implement zooming in and out

class Terrain():
    instance = None

    class __Terrain(pyglet.event.EventDispatcher):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.register_event_type("on_update")
            
            self.loaded_chunks = {}
            self.chunks = {}

        def update(self, player_x, player_y, player_z):
            self.update_chunks_on_screen(player_x, player_y, player_z)

        def set_pos(self, x, y, z):
            for chunk in self.chunks:
                chunk.set_pos(x, y, z)

        def load_chunks_around(self, x, y, z):
            w = constants.SCREEN_WIDTH // 2
            h = constants.SCREEN_HEIGHT // 2

            corners = []
            # Get chunk positions for lower left and upper right corner corners
            for pair in [(-1, -1), (1, 1)]:
                corners.append(self.get_chunkpos_at(pair[0] * w + x, pair[1] * h + y))

            old_keys = self.loaded_chunks.keys() if self.loaded_chunks else []
            new_keys = []
            for tx in range(corners[0][0], corners[1][0] + 1):
                for ty in range(corners[0][1], corners[1][1] + 1):
                    for tz in range(z - 2, z + 1):
                        new_keys.append((tx, ty, tz))

            # Load new chunks
            for chunkx, chunky, chunkz in new_keys:
                # Check if chunk is already loaded
                if (chunkx, chunky, chunkz) not in self.loaded_chunks.keys():
                    print(f"loading {(chunkx, chunky, chunkz)}")
                    self.load_chunk(chunkx, chunky, chunkz)

            # Unload old chunks
            to_remove = list(set(old_keys) - set(new_keys))
            for key in to_remove:
                print(f"unloading {(chunkx, chunky, chunkz)}")
                self.unload_chunk(key)
                            
                        
        def load_chunk(self, chunkx, chunky, chunkz):
            self.loaded_chunks[(chunkx, chunky, chunkz)] = chunk.Chunk(chunkx, chunky, chunkz)

        def unload_chunk(self, key):
            self.loaded_chunks[key].save()
            try:
                self.loaded_chunks[key].delete()
            except:
                pass
            del self.loaded_chunks[key]

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
        

        def update_chunks_on_screen(self, player_x, player_y, player_z):
            min_x = int(player_x - constants.SCREEN_WIDTH // 2)
            min_y = int(player_y - constants.SCREEN_HEIGHT // 2)
            max_x = int(player_x + constants.SCREEN_WIDTH // 2 + constants.TILE_SIZE // 2)
            max_y = int(player_y + constants.SCREEN_HEIGHT // 2 + constants.TILE_SIZE // 2)

            chunk_min_x = int(min_x // constants.TILE_SIZE) // constants.CHUNK_SIZE
            chunk_min_y = int(min_y // constants.TILE_SIZE) // constants.CHUNK_SIZE
            chunk_max_x = int(max_x // constants.TILE_SIZE) // constants.CHUNK_SIZE + 1
            chunk_max_y = int(max_y // constants.TILE_SIZE) // constants.CHUNK_SIZE + 1

            offset_x = min_x % (constants.CHUNK_SIZE * constants.TILE_SIZE)
            offset_y = min_y % (constants.CHUNK_SIZE * constants.TILE_SIZE)


            old_keys = self.chunks.keys() if self.chunks else []
            new_keys = []


            # Generate chunks
            for z in range(player_z+1, player_z-2, -1):
                for x in range(chunk_min_x, chunk_max_x):
                    for y in range(chunk_min_y, chunk_max_y):
                        new_keys.append((x, y, z))
                        if ((x, y, z) in old_keys):
                            c = self.chunks[(x, y, z)]
                        else:
                            c = chunk.Chunk(x, y, z)
                            c.push_handlers(on_update=self.on_tile_update)
                            self.chunks[(x, y, z)] = c

                        c.set_pos((x - chunk_min_x) * constants.CHUNK_SIZE * constants.TILE_SIZE - offset_x,
                                  (y - chunk_min_y) * constants.CHUNK_SIZE * constants.TILE_SIZE - offset_y, z - player_z)

            # Remove chunks outside screen
            to_remove = set(old_keys) - set(new_keys)
            for key in to_remove:
                self.chunks[key].save()
                try:
                    self.chunks[key].delete()
                except:
                    pass
                del self.chunks[key]
    

    def __init__(self, *args, **kwargs):
        if not Terrain.instance:
            Terrain.instance = Terrain.__Terrain(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.instance, name)
