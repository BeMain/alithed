import numpy as np
from perlin_noise import PerlinNoise
import pyfastnoisesimd as fns

from game import constants, debug
from game.positions import Size2, Pos3


threshold = 0.55
freq = Pos3(2, 2, 4)

noise = fns.Noise(seed=constants.SEED)

def generate_chunk(chunkpos):
    global noise
    global threshold
    global freq

    # Generate noise
    size = Size2.chunk_tiles() * freq
    startpos = chunkpos * freq * Size2.chunk_tiles()

    pixels = noise.genAsGrid(shape=size.to_coords(), start=startpos.to_coords()) + 0.5

    # Turn 2d array of int -> 1d array of dict
    tiles = []
    for x in range(constants.CHUNK_SIZE):
        for y in range(constants.CHUNK_SIZE):
            tiles.append(_tile(pixels[x * freq.x, y * freq.y]))

    return np.array(tiles)


def _tile(pixel):
    return {
        "material": ("stone" if pixel >= threshold else "air"),
    }