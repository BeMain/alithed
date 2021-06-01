from game import game_window, debug, positions


if __name__ == "__main__":
    # Enable some debugging functions
    if debug.CLEAR_WORLD_ON_STARTUP:
        data_handler.clear_chunks()
        data_handler.clear_player_data()

    # Start the application
    window = game_window.GameWindow()
    window.run()