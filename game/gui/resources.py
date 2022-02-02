import pyglet
from pyglet.resource import texture

# Constants
GUI_PATH = "gui"
WHITE_BORDER_PATH = "white_border"

pyglet.resource.path = ["resources"]
pyglet.resource.reindex()

# Load images for backgrounds
# Load as textures instead of images to take up less space
white_border = {
    "top": texture(f"{GUI_PATH}/{WHITE_BORDER_PATH}/top.png"),
    "bottom": texture(f"{GUI_PATH}/{WHITE_BORDER_PATH}/bottom.png"),
    "right": texture(f"{GUI_PATH}/{WHITE_BORDER_PATH}/right.png"),
    "left": texture(f"{GUI_PATH}/{WHITE_BORDER_PATH}/left.png"),

    "tr": texture(f"{GUI_PATH}/{WHITE_BORDER_PATH}/top_right.png"),
    "tl": texture(f"{GUI_PATH}/{WHITE_BORDER_PATH}/top_left.png"),
    "br": texture(f"{GUI_PATH}/{WHITE_BORDER_PATH}/bottom_right.png"),
    "bl": texture(f"{GUI_PATH}/{WHITE_BORDER_PATH}/bottom_left.png"),
}
