import pyglet
from pyglet.window import key

from game import constants, debug, positions
from .chunk import Chunk


# TODO: Implement zooming in and out

class Terrain(pyglet.event.EventDispatcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.update_needed = True
        
        self.chunks = {}

    def queue_update(self):
        self.update_needed = True

    def update(self, playerpos):
        if not self.update_needed:
            return
        self.set_pos(playerpos)
        self.update_needed = False

    def set_pos(self, playerpos):
        self.load_chunks_on_screen(playerpos)

        for chunk in self.chunks.values():
            chunk.set_pos(playerpos)

    def load_chunks_on_screen(self, pos):
        # Get chunk positions for lower left and upper right corner
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

        # Load new chunks
        for key in new_keys:
            if key not in self.chunks.keys():
                debug.log(f"Loading chunk {key}", priority=3)
                self.load_chunk_at(positions.Chunkpos.from_str(key))

        # Unload old chunks
        to_remove = list(set(old_keys) - set(new_keys))
        for key in to_remove:
            debug.log(f"Unloading chunk {key}", priority=3)
            self.unload_chunk_at(positions.Chunkpos.from_str(key))

                    
    def load_chunk_at(self, chunkpos):
        chunk = Chunk(chunkpos)
        chunk.push_handlers(on_update=self.on_tile_update)
        self.chunks[str(chunkpos)] = chunk

    def unload_chunk_at(self, chunkpos):
        self.chunks[str(chunkpos)].delete()
        del self.chunks[str(chunkpos)]


    def on_tile_update(self, chunkpos, tilepos):
        self.queue_update()

    def get_tile(self, worldpos):
        chunkpos = worldpos.to_chunkpos()
        tilepos = worldpos.to_tilepos()

        # Make sure tilepos is within bounds
        tilepos.loop_around(positions.Size2.chunk_tiles())

        try:        # Just grab the correct chunk
            chunk = self.chunks[str(chunkpos)]
        except:     # Load the chunk from memory
            chunk = Chunk(chunkpos)
        
        tile = chunk.get_tile(tilepos)
        return tile
