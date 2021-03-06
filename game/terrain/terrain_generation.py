# Using Python 3.7.4
import noise

from game import constants


threshold = 0.55
octaves = 2
freq = 16.0 * octaves

# Updated for 3d-terrain
def generate_chunk(chunk_x, chunk_y, chunk_z):
    global threshold
    global octaves
    global freq

    world_x = chunk_x * constants.CHUNK_SIZE + constants.SEED
    world_y = chunk_y * constants.CHUNK_SIZE + constants.SEED
    world_z = chunk_z * 4 + constants.SEED

    chunk = []
    
    for x in range(constants.CHUNK_SIZE):
        col = []
        for y in range(constants.CHUNK_SIZE):
            pixel = noise.pnoise3((world_x + x) / freq, (world_y + y) / freq, (world_z) / freq, octaves=octaves) * 0.5 + 0.5
            t_data = {
                "material": (1 if pixel >= threshold else 0),
                "tile_x": x,
                "tile_y": y,
            }

            col.append(t_data)
        chunk.append(col)

    return chunk
