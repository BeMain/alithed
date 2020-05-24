# Using Python 3.7.4
from noise import pnoise2, snoise2

from game import constants


threshold = 0.55
octaves = 2
freq = 16.0 * octaves


def generate_chunk(chunk_x, chunk_y):
    global threshold
    global octaves
    global freq

    world_x = chunk_x * constants.CHUNK_SIZE
    world_y = chunk_y * constants.CHUNK_SIZE

    chunk = []
    for x in range(constants.CHUNK_SIZE):
        col = []
        for y in range(constants.CHUNK_SIZE):
            pixel = pnoise2((world_x + x) / freq,
                            (world_y + y) / freq, octaves) * 0.5 + 0.5
            t_data = {}

            t_data["color"] = (1 if pixel >= threshold else 0)
            #t_data["color"] = pixel
            t_data["local_x"] = x
            t_data["local_y"] = y

            col.append(t_data)
        chunk.append(col)

    return chunk