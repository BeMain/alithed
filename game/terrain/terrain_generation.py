import numpy as np
from perlin_noise import PerlinNoise
import pyfastnoisesimd as fns

from game import constants, debug
from game.positions import Size2, Pos3


octaves = 2
threshold = 0.55
freq = Pos3(2, 2, 4)

noise = fns.Noise(seed=constants.SEED, numWorkers=4)

def generate_chunk(chunkpos):
    global noise
    global threshold
    global freq

    size = Size2.chunk_tiles() * freq
    startpos = chunkpos * freq * Size2.chunk_tiles()

    pixels = noise.genAsGrid(shape=size.to_coords(), start=startpos.to_coords()) + 0.5
    
    tiles = []

    for x in range(constants.CHUNK_SIZE):
        for y in range(constants.CHUNK_SIZE):
            tiles.append(_tile(pixels[x * freq.x, y * freq.y], x, y))

    return np.array(tiles)


def _tile(pixel, x, y):
    return {
        "value": pixel,
        "material": ("stone" if pixel >= threshold else "air"),
    }