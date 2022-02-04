from game.positions.classes import Size2

# TODO: Make these selectable within a main menu

SCREEN_SIZE = Size2(800, 600)

FPS = 60


TILE_SIZE = Size2(60, 60)
CHUNK_N_TILES = Size2(16, 16)
CHUNK_SIZE = TILE_SIZE * CHUNK_N_TILES

SEED = 1111


# File structure
CHUNKS_PATH = "save/chunks/"
PLAYER_DATA_PATH = "save/player.json"
ITEMS_PATH = "save/items.json"
