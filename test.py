import numpy as np

from game import debug
from game.positions import *
from game.terrain import tile

# === BENCHMARKS BEFORE ===
# Creating Screenpos: 8.58306884765625e-06
# Creating Screenpos + Worldpos: 1.3589859008789062e-05
# + converting Screenpos -> Worldpos: 3.719329833984375e-05
# + converting Worldpos -> tilepos (test1): 6.437301635742188e-05
# Creating Pos3: 8.106231689453125e-06
# + Creating Pos3 from Pos3 (test2): 1.1205673217773438e-05

# === BENCHMARKS AFTER ===
# Creating Screenpos: 6.9141387939453125e-06
# Creating Screenpos + Worldpos: 9.298324584960938e-06
# + converting Screenpos -> Worldpos: 2.3603439331054688e-05
# + converting Worldpos -> tilepos (test1): 3.647804260253906e-05


@debug.timeit
def test1():
    screenpos = Screenpos(1, 2)
    playerpos = Worldpos(0, 0, 0)
    worldpos = screenpos.to_worldpos(playerpos)
    tilepos = worldpos.to_tilepos()


@debug.timeit
def test2():
    posa = Pos3(1, 2, 3)
    posb = Pos3.from_pos3(posa)


test1()
