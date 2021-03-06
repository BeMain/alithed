from game import game_window, constants
from game.terrain import data_handler


if __name__ == "__main__":
    # Enable some debugging functions
    if constants.DEBUG_CLEAR_WORLD_ON_STARTUP:
        data_handler.clear_chunks()
        data_handler.clear_player_data()

    # Start the application
    window = game_window.GameWindow()
    window.run()