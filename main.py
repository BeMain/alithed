from game import game_window, debug, positions
from game.terrain.data_handler import clear_chunks, clear_player_data


if __name__ == "__main__":
    # Enable debugging functions
    if debug.CLEAR_WORLD_ON_STARTUP:
        clear_chunks()
        clear_player_data()

    # Start application
    window = game_window.GameWindow()
    window.run()