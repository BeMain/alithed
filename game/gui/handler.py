import glooey

from game import constants
from game.gui import menus, pause, inventory


class GuiHandler(glooey.Gui):
    def __init__(self, *args, **kwargs):
        super(GuiHandler, self).__init__(*args, **kwargs)
        
        self.menus = []
        self.inventory = inventory.Inventory(self)
        

    def close_menus(self):
        pause.paused = False
        self.clear()
        self.menus = []
    
    def _open_menu(self, menu):
        pause.paused = True
        self.inventory.close()
        self.clear()

        self.add(menu)
        self.menus.append(menu)


    def open_main_menu(self):
        menu = menus.MainMenu()
        self._open_menu(menu)
        
        @menu.event
        def on_button_click(action):
            if action == "Continue":
                self.close_menus()
            elif action == "Settings":
                self.open_settings()
            elif action == "Exit":
                self.get_window().exit()

            else: 
                print("Unknown action:", action)

    
    def open_settings(self):
        menu = menus.Settings()
        self._open_menu(menu)

        @menu.event
        def on_setting_changed(setting):
            if setting == "SCREEN_HEIGHT":
                self.get_window().height = constants.SCREEN_HEIGHT
            elif setting == "SCREEN_WIDTH":
                self.get_window().width = constants.SCREEN_WIDTH
        
        @menu.event
        def on_button_click(action):
            if action == "Back":
                self.open_main_menu()
            if action == "Done":
                self.close_menus()

