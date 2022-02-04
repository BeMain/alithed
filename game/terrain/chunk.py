import asyncio
import numpy as np
import pyglet
import time

from game import constants, debug
from game.terrain import data_handler
from game.positions import Tilepos
from .tile import Tile


class Chunk(pyglet.event.EventDispatcher):
    def __init__(self, chunkpos):
        super(Chunk, self).__init__()

        self.register_event_type("on_update")

        self.chunkpos = chunkpos

        self.tiles = np.zeros(constants.CHUNK_SIZE.width *
                              constants.CHUNK_SIZE.height)
        self.load_tiles_task = asyncio.create_task(self._load_tiles())
        self.is_loaded = False

    async def _load_tiles(self):
        if self.is_loaded:
            return

        chunk = await data_handler.load_chunk(self.chunkpos)
        # Turn the array of dicts -> array of Tiles
        self.tiles = np.array([self._load_tile(tile, idx)
                              for idx, tile in enumerate(chunk)])
        self.is_loaded = True

    def _load_tile(self, *args):
        tile = Tile.from_data(*args)
        tile.push_handlers(on_update=self.on_tile_update)
        return tile

    def on_tile_update(self, tilepos):
        self.dispatch_event("on_update", self.chunkpos, tilepos)

    def get_tile(self, tilepos):
        return self.tiles[tilepos.to_index()]

    def set_pos(self, playerpos):
        if not self.is_loaded:
            return

        screenpos = self.chunkpos.to_screenpos(playerpos)
        for tile in self.tiles:
            # TODO: Don't render if block above
            tile.set_pos(screenpos, self.chunkpos.z - playerpos.z)

    def to_data(self):
        return [tile.to_data() for tile in self.tiles]

    async def delete(self):
        if not self.is_loaded:
            self.load_tiles_task.cancel()
            return

        self.is_loaded = False
        self.batch = None
        await self.save()

        try:    # Delete tiles
            for tile in self.tiles:
                tile.delete()
        except:
            debug.log("Error deleting tiles", priority=1)

    async def save(self):
        await data_handler.write_chunk(self.chunkpos, self.to_data())
