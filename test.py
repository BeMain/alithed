import numpy as np

from game import debug
from game.positions import Tilepos



arr = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])

for x in np.nditer(arr):
  print(x)
