import os

import pyglet
from pyglet import gl

from game import constants, items


pyglet.resource.path = ["resources"]
pyglet.resource.reindex()

# We don't want images to be blurry when scaled
gl.glEnable(gl.GL_TEXTURE_2D)
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)


def center_image(image):
    # Sets an image's anchor point to its center
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

def get_background_scale_factor(background):
    # Used to scale background to fill screen
    scale_x = constants.SCREEN_WIDTH / background.width
    scale_y = constants.SCREEN_HEIGHT / background.height
    return max(scale_x, scale_y)

def get_tile_image(path):
    img = pyglet.resource.image(path)
    img.width = img.height = constants.TILE_SIZE
    center_image(img)
    return img


player_image = pyglet.resource.image("player.png")
player_image.width /= 10
player_image.height /= 10
center_image(player_image)


# Load tile textures
tiles = {}
for tile in items.items:
    path = f"tiles/{tile}.png"
    if os.path.exists("resources/"+path):
        tiles[items.items[tile]["texture_id"]] = get_tile_image(path)


# Load background image
background_image = pyglet.resource.image("backgrounds/space.png")
scale_factor = get_background_scale_factor(background_image)
background_image.width *= scale_factor
background_image.height *= scale_factor
background_image.anchor_x = 0
background_image.anchor_y = 0
