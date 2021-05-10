# Using Python 3.7.4
import perlin_noise

from game import constants


octaves = 2
threshold = 0.55
freq = 16.0 * octaves

noise = perlin_noise.PerlinNoise(octaves=octaves, seed=constants.SEED)

# Updated for 3d-terrain
def generate_chunk(chunk_x, chunk_y, chunk_z):
    global noise
    global threshold
    global freq

    world_x = chunk_x * constants.CHUNK_SIZE
    world_y = chunk_y * constants.CHUNK_SIZE
    world_z = chunk_z * 4

    chunk = []
    
    for x in range(constants.CHUNK_SIZE):
        col = []
        for y in range(constants.CHUNK_SIZE):
            pixel = noise([(world_x + x) / freq, (world_y + y) / freq, (world_z) / freq]) * 0.5 + 0.5
            t_data = {
                "value": pixel,
                "material": ("stone" if pixel >= threshold else "air"),
                "tile_x": x,
                "tile_y": y,
            }

            col.append(t_data)
        chunk.append(col)

    return chunk
