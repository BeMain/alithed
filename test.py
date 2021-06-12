from perlin_noise import PerlinNoise
import pyfastnoisesimd as fns

from game import debug


@debug.timeit
def gen_fastnoise(n):
    shape = [1, n, n]
    
    noise = fns.Noise(seed=100, numWorkers=4)
    return noise.genAsGrid(shape=shape, start=[0,0,0])

print(gen_fastnoise(4))
print(gen_fastnoise(16) + 1)