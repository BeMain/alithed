import numpy as np
import pyfastnoisesimd as fns

from game import constants, debug
from game.positions import Pos3


threshold = 0.55
freq = Pos3(2, 2, 4)

noise = fns.Noise(seed=constants.SEED)


def generate_chunk(chunkpos):
    global noise
    global threshold
    global freq

    # Generate noise
    size = constants.CHUNK_N_TILES * freq
    startpos = chunkpos * freq * constants.CHUNK_N_TILES

    pixels = noise.genAsGrid(shape=[*size], start=[*startpos]) + 0.5

    # Turn 2d array of int -> 1d array of dict
    tiles = []
    for x in range(constants.CHUNK_N_TILES.width):
        for y in range(constants.CHUNK_N_TILES.height):
            tiles.append(_tile(pixels[x * freq.x, y * freq.y]))

    return np.array(tiles)


def _tile(pixel):
    return {
        "material": ("stone" if pixel >= threshold else "air"),
    }
