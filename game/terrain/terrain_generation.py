import perlin_noise

from game import constants, positions, classes


octaves = 2
threshold = 0.55
freq = 16.0 * octaves

noise = perlin_noise.PerlinNoise(octaves=octaves, seed=constants.SEED)

# Updated for 3d-terrain
def generate_chunk(chunkpos):
    global noise
    global threshold
    global freq

    worldpos = chunkpos * classes.Pos3(constants.CHUNK_SIZE, constants.CHUNK_SIZE, 4)

    chunk = []
    
    for x in range(constants.CHUNK_SIZE):
        col = []
        for y in range(constants.CHUNK_SIZE):
            pixel = noise([(worldpos.x + x) / freq, (worldpos.y + y) / freq, (worldpos.z) / freq]) * 0.5 + 0.5
            t_data = {
                "value": pixel,
                "material": ("stone" if pixel >= threshold else "air"),
                "tilepos": positions.Tilepos(x, y).to_list()
            }

            col.append(t_data)
        chunk.append(col)

    return chunk
