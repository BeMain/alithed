import math

from game import constants


def clamp(my_value, min_value, max_value):
    return max(min(my_value, max_value), min_value)

def distancesq(pos1, pos2):
    return (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2

def angle_between(pos1, pos2):
    x = pos1[0] - pos2[0]
    y = pos1[1] - pos2[1]
    return -math.degrees(math.atan2(y, x))


def to_screenpos(worldpos, playerpos):
    x = worldpos[0] - playerpos[0] + constants.SCREEN_WIDTH // 2
    y = worldpos[1] - playerpos[1] + constants.SCREEN_HEIGHT // 2
    return (x, y)
