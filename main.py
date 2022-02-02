import asyncio

from game import game_window, debug
from game.terrain import async_data_handler


if __name__ == "__main__":
    # Enable debugging functions
    if debug.CLEAR_WORLD_ON_STARTUP:
        async_data_handler.clear_chunks()
        async_data_handler.clear_player_data()

    # Start application
    window = game_window.GameWindow()
    asyncio.run(window.run())
