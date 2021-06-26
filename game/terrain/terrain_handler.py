import math
import numpy as np
import time
import itertools
import asyncio

import pyglet
from pyglet.window import key

from game import constants, debug, positions
from .chunk import Chunk


# TODO: Implement zooming in and out

class Terrain(pyglet.event.EventDispatcher):
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

    def load_chunks_on_screen(self, pos):
        # Get chunk positions for lower left and upper right corner corners
        corners = []
        for rel_cords in [(-1, -1), (1, 1)]:
            worldpos = pos + positions.Pos2.from_list(rel_cords) * positions.Size2.screensize() // 2
            chunkpos = worldpos.to_chunkpos()
            corners.append(chunkpos)

        old_keys = self.chunks.keys() if self.chunks else []
        # Get positions for chunks on screen
        new_keys = []
        for x in range(corners[0].x, corners[1].x + 1):
            for y in range(corners[0].y, corners[1].y + 1):
                for z in range(pos.z - 1, pos.z + 2):
                    new_keys.append(str((x, y, z)))

        asyncio.run(self.load_chunks(new_keys))

        # Unload old chunks
        to_remove = list(set(old_keys) - set(new_keys))
        for key in to_remove:
            debug.log(f"Unloading chunk {key}")
            self.unload_chunk_at(positions.Chunkpos.from_str(key))
                        
    async def load_chunks(self, keys):
        asyncio.gather(*(self.load_chunk(key) for key in keys))

    async def load_chunk(self, key):
        # Load new chunk
        if key not in self.chunks.keys():
            debug.log(f"Loading chunk {key}")
            c = Chunk(positions.Chunkpos.from_str(key))
            await c.load_tiles()
            c.push_handlers(on_update=self.on_tile_update)
            self.chunks[str(key)] = c

    def unload_chunk_at(self, chunkpos):
        self.chunks[str(chunkpos)].save()
        self.chunks[str(chunkpos)].delete()
        del self.chunks[str(chunkpos)]


    def on_tile_update(self, chunkpos, tilepos):
        self.dispatch_event("on_update", chunkpos, tilepos)

    def get_tile(self, worldpos):
        chunkpos = worldpos.to_chunkpos()
        tilepos = worldpos.to_tilepos()

        # Make sure tilepos is within bounds
        tilepos.loop_around(positions.Size2.chunk_tiles())

        try:
            # Just grab the correct chunk
            c = self.chunks[str(chunkpos)]
        except:
            # Load the chunk from memory
            c = Chunk(chunkpos)
            asyncio.run(c.load_tiles())
        
        tile = c.tiles[tilepos.x][tilepos.y]
        return tile
