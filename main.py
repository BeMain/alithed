import asyncio

from game import debug, game_window
from game.terrain import data_handler

if __name__ == "__main__":
    # Enable debugging functions
    if debug.CLEAR_WORLD_ON_STARTUP:
        data_handler.clear_chunks()
        data_handler.clear_player_data()

    # Start application
    window = game_window.GameWindow()
    asyncio.run(window.run())
