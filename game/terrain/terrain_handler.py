import asyncio
import pyglet

from game import debug, constants
from game.positions import Chunkpos, Pos2
from .chunk import Chunk

# TODO: Implement zooming in and out


class Terrain(pyglet.event.EventDispatcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.update_needed = True

        self.chunks = {}

    def queue_update(self):
        self.update_needed = True

    async def update(self, playerpos):
        if not self.update_needed:
            return
        await self.set_pos(playerpos)
        self.update_needed = False

    async def set_pos(self, playerpos):
        self.passive_load_chunks(playerpos)
        await self.activate_chunks_on_screen(playerpos)

        for chunk in self.chunks.values():
            chunk.set_pos(playerpos)

    def passive_load_chunks(self, pos):
        # Get chunk positions for lower left and upper right corner
        corners = []
        for rel_cords in [(-2, -2), (2, 2)]:
            worldpos = pos + Pos2(*rel_cords) * constants.SCREEN_SIZE // 2
            chunkpos = worldpos.to_chunkpos()
            corners.append(chunkpos)

        old_keys = self.chunks.keys() if self.chunks else []
        # Get positions for chunks within selected area
        new_keys = []
        for x in range(corners[0].x, corners[1].x + 1):
            for y in range(corners[0].y, corners[1].y + 1):
                for z in range(pos.z - 2, pos.z + 2):
                    new_keys.append(str((x, y, z)))

        # Load new chunks
        for key in new_keys:
            if key not in self.chunks.keys():
                debug.log(f"Loading chunk {key}", priority=3)
                self.load_chunk_at(Chunkpos.from_str(key))

         # Unload old chunks
        to_remove = list(set(old_keys) - set(new_keys))
        for key in to_remove:
            debug.log(f"Unloading chunk {key}", priority=3)
            self.unload_chunk_at(Chunkpos.from_str(key))

    async def activate_chunks_on_screen(self, pos):
        # Get chunk positions for lower left and upper right corner
        corners = []
        for rel_cords in [(-1, -1), (1, 1)]:
            worldpos = pos + Pos2(*rel_cords) * constants.SCREEN_SIZE // 2
            chunkpos = worldpos.to_chunkpos()
            corners.append(chunkpos)

        # Get positions for chunks on screen
        new_keys = []
        for x in range(corners[0].x, corners[1].x + 1):
            for y in range(corners[0].y, corners[1].y + 1):
                for z in range(pos.z - 1, pos.z + 2):
                    # Activate chunk
                    key = str((x, y, z))
                    if not self.chunks[key].is_loaded:
                        debug.log(f"Activating chunk {key}", priority=3)
                        await self.chunks[key].load_tiles_task

    def load_chunk_at(self, chunkpos):
        chunk = Chunk(chunkpos)
        chunk.push_handlers(on_update=self.on_tile_update)
        self.chunks[str(chunkpos)] = chunk

    def unload_chunk_at(self, chunkpos):
        asyncio.create_task(self.chunks[str(chunkpos)].delete())
        del self.chunks[str(chunkpos)]

    def on_tile_update(self, chunkpos, tilepos):
        self.queue_update()

    async def get_tile(self, worldpos):
        chunkpos = worldpos.to_chunkpos()
        tilepos = worldpos.to_tilepos()

        # Make sure tilepos is within bounds
        tilepos %= constants.CHUNK_N_TILES

        try:        # Just grab the correct chunk
            chunk = self.chunks[str(chunkpos)]
            if not chunk.is_loaded:
                await chunk.load_tiles_task
        except:     # Load the chunk from memory
            chunk = Chunk(chunkpos)
            await chunk.load_tiles_task

        tile = chunk.get_tile(tilepos)
        return tile
